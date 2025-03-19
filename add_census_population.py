# Run from command-line: 
#  python3 add_census_population.py "/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Downloads/Combined Datasets/Commuter Vehicles by city.csv" --api-key c6626ccdcb7542e94909cec187af575af3fc4693

# python3 add_census_population.py "/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Downloads/Combined Datasets/Commuter Vehicles by city.csv" --api-key c6626ccdcb7542e94909cec187af575af3fc4693 --debug
# 

#!/usr/bin/env python3
"""
Census Population Data Enrichment Script

This script reads a CSV file containing GEO_ID data, fetches the latest population
estimates from the US Census API for each GEO_ID, and adds this data as a new
'Population' column to the CSV file.

It handles the specific format of the "Commuter Vehicles by city.csv" file,
which includes header rows and census variable columns.
"""

import pandas as pd
import requests
import argparse
import os
from typing import List, Dict, Optional, Any
import time
import re


def extract_state_place_from_geoid(geo_id: str) -> tuple:
    """
    Extract state and place codes from a Census GEO_ID.
    
    Args:
        geo_id: Census GEO_ID (format: 1600000US[state code][place code])
        
    Returns:
        Tuple of (state_code, place_code)
    """
    # GEO_IDs for places follow the format 1600000US[state code][place code]
    # State code is 2 digits, place code is 5 digits
    if geo_id.startswith('1600000US'):
        # Extract the part after "1600000US"
        code_part = geo_id[9:]
        if len(code_part) >= 7:
            state_code = code_part[:2]
            place_code = code_part[2:7]
            return state_code, place_code
    
    return None, None


def fetch_population_data(geo_ids: List[str], api_key: Optional[str] = None, debug: bool = False) -> Dict[str, int]:
    """
    Fetch population data from the US Census API for a list of GEO_IDs.
    
    Args:
        geo_ids: List of GEO_IDs to fetch population data for
        api_key: Optional Census API key
        
    Returns:
        Dictionary mapping GEO_IDs to population values
    """
    # Latest available ACS 5-year estimates (as of March 2025)
    year = 2023  # Most recent available year 
    dataset = "acs/acs5"
    
    # Base URL for Census API
    base_url = f"https://api.census.gov/data/{year}/{dataset}"
    
    population_data = {}
    
    # Group GEO_IDs by state to make more efficient API calls
    state_place_map = {}
    for geo_id in geo_ids:
        state_code, place_code = extract_state_place_from_geoid(geo_id)
        if state_code and place_code:
            if state_code not in state_place_map:
                state_place_map[state_code] = []
            state_place_map[state_code].append((geo_id, place_code))
    
    # Process each state separately
    for state_code, places in state_place_map.items():
        # Process places in batches to avoid query string length limits
        batch_size = 50
        for i in range(0, len(places), batch_size):
            batch_places = places[i:i+batch_size]
            
            # Extract place codes for this batch
            place_codes = [place_code for _, place_code in batch_places]
            place_list = ",".join(place_codes)
            
            # Construct the query parameters
            params = {
                "get": "NAME,B01003_001E",  # B01003_001E is the total population estimate
                "for": f"place:{place_list}",
                "in": f"state:{state_code}"
            }
            
            # Add API key if provided
            if api_key:
                params["key"] = api_key
            
            try:
                # Make the API request
                if debug:
                    print(f"API Request URL: {base_url}")
                    print(f"Params: {params}")
                
                response = requests.get(base_url, params=params)
                
                if debug:
                    print(f"Response status: {response.status_code}")
                    print(f"Response content: {response.text[:1000]}") # Print first 1000 chars
                
                response.raise_for_status()
                
                # Parse the response
                data = response.json()
                
                # Skip if only headers are returned (no data)
                if len(data) <= 1:
                    if debug:
                        print("No data returned in response (only headers)")
                    continue
                
                # Extract headers and data
                headers = data[0]
                rows = data[1:]
                
                # Find indexes for place, state, and population columns
                name_index = headers.index("NAME")
                pop_index = headers.index("B01003_001E")
                place_index = headers.index("place")
                state_index = headers.index("state")
                
                # Create a mapping of place codes to populations
                place_pop_map = {}
                for row in rows:
                    state = row[state_index]
                    place = row[place_index]
                    population = int(row[pop_index])
                    place_pop_map[(state, place)] = population
                
                # Map the populations back to the original GEO_IDs
                for geo_id, place_code in batch_places:
                    key = (state_code, place_code)
                    if key in place_pop_map:
                        population_data[geo_id] = place_pop_map[key]
                
                print(f"Processed {len(batch_places)} places in state {state_code}")
                
                # Sleep briefly to avoid hitting API rate limits
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error fetching batch for state {state_code}: {str(e)}")
                print(f"API URL: {base_url}")
                print(f"Params: {params}")
    
    return population_data


def add_population_to_csv(input_file: str, output_file: Optional[str] = None, api_key: Optional[str] = None, debug: bool = False) -> None:
    """
    Add population data from the Census API to a CSV file.
    
    Args:
        input_file: Path to the input CSV file containing GEO_ID column
        output_file: Path to the output CSV file (if None, will modify the input file)
        api_key: Optional Census API key
    """
    # Determine output file path
    if output_file is None:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_with_population{ext}"
    
    # Read the CSV file
    try:
        # First read to inspect - use the first few rows to determine if there are header rows
        sample_df = pd.read_csv(input_file, nrows=5)
        
        # In the Commuter Vehicles by city.csv file, there might be metadata rows
        # Check if the first row contains "Geography" or doesn't look like regular data
        if 'GEO_ID' in sample_df.columns and (
            sample_df.iloc[0]['GEO_ID'] == 'Geography' or
            not str(sample_df.iloc[0]['GEO_ID']).startswith('1600000US')
        ):
            # Try to find the first row with actual data (starting with 1600000US)
            skip_rows = 0
            for i in range(min(5, len(sample_df))):
                if str(sample_df.iloc[i]['GEO_ID']).startswith('1600000US'):
                    skip_rows = i
                    break
            
            # Re-read the file, skipping the descriptive header rows
            df = pd.read_csv(input_file, skiprows=skip_rows)
            print(f"Skipped {skip_rows} descriptive header row(s)")
        else:
            # Read the file normally
            df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return
    
    # Check if GEO_ID column exists
    if 'GEO_ID' not in df.columns:
        print("Error: CSV file does not contain a 'GEO_ID' column")
        return
    
    # Filter out any rows that don't have proper GEO_IDs
    valid_geo_ids = df['GEO_ID'].str.startswith('1600000US')
    if not valid_geo_ids.all():
        print(f"Filtering out {(~valid_geo_ids).sum()} rows with invalid GEO_IDs")
        df = df[valid_geo_ids]
    
    # Get unique GEO_IDs
    unique_geo_ids = df['GEO_ID'].unique().tolist()
    
    print(f"Fetching population data for {len(unique_geo_ids)} unique GEO_IDs...")
    
    # Fetch population data
    population_data = fetch_population_data(unique_geo_ids, api_key, debug)
    
    print(f"Retrieved population data for {len(population_data)} out of {len(unique_geo_ids)} GEO_IDs")
    
    # Add population data as a new column
    df['Population'] = df['GEO_ID'].map(population_data)
    
    # Count and report how many places got population data
    places_with_pop = df['Population'].notna().sum()
    print(f"{places_with_pop} out of {len(df)} places have population data")
    
    # Show a sample of the data with population
    print("\nSample of data with population:")
    # Check which columns are available for display
    display_cols = ['GEO_ID', 'Population']
    if 'NAME' in df.columns:
        display_cols.insert(1, 'NAME')
    print(df[display_cols].head(5).to_string())
    
    # Calculate some statistics to verify the data looks reasonable
    if 'Population' in df.columns:
        pop_stats = df['Population'].describe()
        print("\nPopulation statistics:")
        print(f"Count: {pop_stats['count']}")
        print(f"Mean: {pop_stats['mean']:.2f}")
        print(f"Min: {pop_stats['min']}")
        print(f"Max: {pop_stats['max']}")
    
    # Save the updated DataFrame
    df.to_csv(output_file, index=False)
    print(f"\nUpdated CSV saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Add Census population data to a CSV file based on GEO_ID")
    parser.add_argument("input_file", help="Path to the input CSV file containing GEO_ID column")
    parser.add_argument("--output", help="Path to the output CSV file (optional)")
    parser.add_argument("--api-key", help="Census API key (optional but recommended)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode with extra logging")
    
    args = parser.parse_args()
    
    add_population_to_csv(args.input_file, args.output, args.api_key, args.debug)


if __name__ == "__main__":
    main()