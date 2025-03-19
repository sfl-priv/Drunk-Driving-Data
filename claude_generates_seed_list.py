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


def fetch_population_data(geo_ids: List[str], api_key: Optional[str] = None) -> Dict[str, int]:
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
    
    # We'll process GEO_IDs in batches to avoid query string length limits
    batch_size = 50
    population_data = {}
    
    # Process GEO_IDs in batches
    for i in range(0, len(geo_ids), batch_size):
        batch_geo_ids = geo_ids[i:i+batch_size]
        
        # Convert the geo_ids list to a comma-separated string for IN clause
        geo_id_list = ",".join([f"'{geo_id}'" for geo_id in batch_geo_ids])
        
        # Construct the query parameters
        params = {
            "get": "GEO_ID,B01003_001E",  # B01003_001E is the total population estimate
            "for": "place:*",
            "in": "state:*",
            "GEO_ID": f"in:({geo_id_list})"
        }
        
        # Add API key if provided
        if api_key:
            params["key"] = api_key
        
        try:
            # Make the API request
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            
            # Skip if only headers are returned (no data)
            if len(data) <= 1:
                continue
            
            # Extract headers and data
            headers = data[0]
            rows = data[1:]
            
            # Find indexes for GEO_ID and population columns
            geo_id_index = headers.index("GEO_ID")
            pop_index = headers.index("B01003_001E")
            
            # Add to results dictionary
            for row in rows:
                geo_id = row[geo_id_index]
                population = int(row[pop_index])
                population_data[geo_id] = population
            
            # Sleep briefly to avoid hitting API rate limits
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Error fetching batch starting with {batch_geo_ids[0]}: {str(e)}")
    
    return population_data


def add_population_to_csv(input_file: str, output_file: Optional[str] = None, api_key: Optional[str] = None) -> None:
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
        # First read to inspect
        df = pd.read_csv(input_file)
        
        # Check if the first row appears to be a descriptive header
        # (In your file, the first row has "Geography" in the GEO_ID column)
        if df.iloc[0]['GEO_ID'] == 'Geography':
            # Re-read the file, skipping the descriptive header row
            df = pd.read_csv(input_file, skiprows=1)
            print("Skipped descriptive header row")
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
    population_data = fetch_population_data(unique_geo_ids, api_key)
    
    print(f"Retrieved population data for {len(population_data)} out of {len(unique_geo_ids)} GEO_IDs")
    
    # Add population data as a new column
    df['Population'] = df['GEO_ID'].map(population_data)
    
    # Count and report how many places got population data
    places_with_pop = df['Population'].notna().sum()
    print(f"{places_with_pop} out of {len(df)} places have population data")
    
    # Save the updated DataFrame
    df.to_csv(output_file, index=False)
    print(f"Updated CSV saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Add Census population data to a CSV file based on GEO_ID")
    parser.add_argument("input_file", help="Path to the input CSV file containing GEO_ID column")
    parser.add_argument("--output", help="Path to the output CSV file (optional)")
    parser.add_argument("--api-key", help="Census API key (optional but recommended)")
    parser.add_argument("--year", type=int, default=2023, 
                        help="Census year to use (default: 2023)")
    
    args = parser.parse_args()
    
    # If running the script on the provided file directly
    if os.path.basename(args.input_file) == "Commuter Vehicles by city.csv":
        print("Detected the Commuter Vehicles by city.csv file")
    
    add_population_to_csv(args.input_file, args.output, args.api_key)


if __name__ == "__main__":
    main()