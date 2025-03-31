import argparse
import pandas as pd
from superfluous_city_list import cities
from get_master_files import concat_fars_ext
import sys

# Usual spot for FARS Data: /Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Downloads/Amanda Demanda - Deadliest Roads in Texas/NHTSA FARS Data

'''

This script goes through FARS data downloads and gives us the counts of a given data point by a list of cities.
The list of cities in this script is currently set to the 100 cities in the US with the most commuter vehicles used on a daily basis as per the US Census.


From the command line the user can choose which files within the FARS download to analyse per the filename args, as well as the data point they want to get counts for as per the column arg.


The script assumes the following:

- That two FARS folders are needed to get the information we need, and that they should be merged on the ST_CASE column
- That the only column for which we need the datapoints is the only one we need to access. State and city are there by default, as well as whether or not the driver was drinking.

To add or remove columns, access the usecols argument in the reader objects in the get_files funciton.

'''

# Define CLI functionality
parser = argparse.ArgumentParser(prog='Find the Deadliest Streets in American Cities', description='Data point to get counts for')
parser.add_argument('-c','--column', metavar='column', type=str, help='Picks a column in the dataset to get counts for')
parser.add_argument('-f0', '--filename_0', metavar='first file name', type=str, help='Picks which file from the FARS datasets to select')
parser.add_argument('-f1', '--filename_1', metavar='second file name', type=str, help='Picks second file which file from the FARS datasets to select if a merge is needed')
args = parser.parse_args()
column = args.column
filename_0 = args.filename_0
filename_1 = args.filename_1

def main():
    
    folder_out = input("Where will the final file go? ")
    filename_out = input("Name your file: ")
    format(create_spreadsheet(filter_data(get_files(filename_0, filename_1)))).to_csv(f'{folder_out}/{filename_out}.csv')

    
def get_files(fn0, fn1):
    
# Get master files, check if reading in worked 
    try:
        first_file = None
        first_file = pd.read_csv(concat_fars_ext(fn0), usecols=['ST_CASE', 'STATENAME', 'CITYNAME', args.column])
        if first_file is not None:
            print(f"Successfuly created {fn0} file")
    except FileNotFoundError: # Catch user typing in wrong file or path
        print(f"Could not find {fn0}, please check spelling and capitalisation is the same across all years in FARS folder.\n Please also check you are using the correct filepath")

    try:
        second_file = None
        second_file = pd.read_csv(concat_fars_ext(fn1), usecols=['ST_CASE', 'DRINKING', 'DRINKINGNAME'])
        if second_file is not None:
            print(f"Successfuly created {fn1} file")
    except FileNotFoundError: # Catch user typing in wrong file or path
        print(f"Could not find {fn1}, please check spelling and capitalisation is the same across all years in FARS folder.\n Please also check you are using the correct filepath")

    print("File reading successful.\nMerging Files.")
    
    # Merge both dataframes
    merged_file = pd.merge(first_file, second_file, on='ST_CASE')
    print("Merge successful")
    
    return merged_file


def filter_data(data):
    
    # Get all unique states in a set
    states_and_cities_csv = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Code/Amanda Demanda - Drunk Driving Hotspots Code/States and Cities.csv")
    states_only = states_and_cities_csv['State']
    states_only.tolist()
    unique_states = set(states_only)

    # Filter for only drunk driving accidents which occur in cities
    print("Filtering merged file")
    filtered_merged_file = data.loc[(data['CITYNAME'] != 'NOT APPLICABLE') & (data['CITYNAME'] != 'Other') & (data['DRINKING'] == 1)]
    state_filtered_file = filtered_merged_file[(filtered_merged_file['STATENAME'].isin(unique_states))] # Make sure no cities in other states are included
    print("Successfully merged files")
    
    return state_filtered_file


def create_spreadsheet(file):

    # Declare final spreadsheet columns as empty lists
    city_col = []
    value_col = []
    count_col = []

    # Prepare dataframe as empty dict with above lists as values
    final_target_dict = {
        'City' : city_col,
        args.column : value_col,
        'Occurence Count' : count_col,
    }

    # Iterate over list of cities
    print("Fetching data for all cities")
    for city in cities:
        try:
            one_city_df = file[file.CITYNAME == f'{city}'] # Filter Dataframe to target city
            city_col.append(f'{city}') # Add city name as spreadsheet row
            value_counts_series = one_city_df[args.column].value_counts() # Show value counts of target value
            highest_count = value_counts_series.index[0] # Get highest count
            count = value_counts_series.iloc[0] # Get count amount
            
            # Add all the extracted data to the lists which will contain our dictionary values
            value_col.append(highest_count)
            count_col.append(count)
            print(f"Successfully added {city} data")
        except IndexError: # Catch city lists not matching
            print(f"Data for {city} not found.\nCheck your list of cities and make sure it matches accident data.\nBe mindful of case sensitivity. ")
            value_col.append("N/A")
            count_col.append("N/A")
            continue # If no match, fill row with values and move on to next city
        
    return final_target_dict


def format(dict):
    
    # Change column name to a more user-friendly name
    new_col_name = input(f"User-firendly column name for {args.column}: ")
    dict[new_col_name] = dict.pop(args.column)

    # Cast dictionary into a Dataframe
    if len(dict['City']) == len(dict[new_col_name]):
        final_target_df = pd.DataFrame(data=dict)
    else:
        sys.exit("Dictionary row lengths do not match, Pandas could not support Dataframe creation.\n") # Catch empty cell values

    # Alphabetically sort cities column
    final_target_df.sort_values('City')
    
    return final_target_df


if __name__ == "__main__":
    main()