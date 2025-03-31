import argparse
import pandas as pd
from superfluous_city_list import cities
from get_master_files import concat_fars_ext
import os

# /Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Downloads/Amanda Demanda - Deadliest Roads in Texas/NHTSA FARS Data
# /Users/sebastianfirrell/Desktop
# filtering (accident)
# filtering (person)

# Define CLI functionality
parser = argparse.ArgumentParser(prog='Find the Deadliest Streets in American Cities', description='Data point to get counts for')
parser.add_argument('-c','--column', metavar='column', type=str, help='Picks a column in the dataset to get counts for')
parser.add_argument('-f0', '--filename_0', metavar='first file name', type=str, help='Picks which file from the FARS datasets to select')
parser.add_argument('-f1', '--filename_1', metavar='second file name', type=str, help='Picks second file which file from the FARS datasets to select if a merge is needed')
args = parser.parse_args()
column = args.column
filename_0 = args.filename_0
filename_1 = args.filename_1

# Get master files, check if reading in worked 
try:
    first_file = None
    first_file = pd.read_csv(concat_fars_ext(args.filename_0), usecols=['ST_CASE', 'STATENAME', 'CITYNAME', args.column])
    if first_file is not None:
        print(f"Successfuly created {args.filename_0} file")
except FileNotFoundError: # Catch user typing in wrong file or path
    print(f"Could not find {args.filename_0}, please check spelling and capitalisation is the same across all years in FARS folder.\n Please also check you are using the correct filepath")

try:
    second_file = None
    second_file = pd.read_csv(concat_fars_ext(args.filename_1), usecols=['ST_CASE', 'DRINKING', 'DRINKINGNAME'])
    if second_file is not None:
        print(f"Successfuly created {args.filename_1} file")
except FileNotFoundError: # Catch user typing in wrong file or path
    print(f"Could not find {args.filename_1}, please check spelling and capitalisation is the same across all years in FARS folder.\n Please also check you are using the correct filepath")


# Merge both dataframes
merged_file = pd.merge(first_file, second_file, on='ST_CASE')

# Get all unique states in a set
states_and_cities_csv = pd.read_csv("States and Cities.csv")
states_only = states_and_cities_csv['State']
states_only.tolist()
unique_states = set(states_only)

# Filter for only drunk driving accidents which occur in cities
filtered_merged_file = merged_file.loc[(merged_file['CITYNAME'] != 'NOT APPLICABLE') & (merged_file['CITYNAME'] != 'Other') & (merged_file['DRINKING'] == 1)]
state_filtered_file = filtered_merged_file[(filtered_merged_file['STATENAME'].isin(unique_states))] # Make sure no cities in other states are included

# Get all unique states in a set
states_and_cities_csv = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Code/Amanda Demanda - Drunk Driving Hotspots Code/States and Cities.csv")
states_only = states_and_cities_csv['State']
states_only.tolist()
unique_states = set(states_only)

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

print(final_target_dict)


'''# Iterate over list of cities
for city in cities:
    one_city_df = state_filtered_file[state_filtered_file.CITYNAME == f'{city}'] # Filter Dataframe to target city
    city_col.append(f'{city}') # Add city name as spreadsheet column
    value_counts_series = one_city_df[args.column].value_counts() # Show value counts of target value
    highest_count = value_counts_series.index[0] # Get highest count
    count = value_counts_series.iloc[0] # Get count amount
    
    # Add all the extracted data to the lists which will contain our dictionary values
    value_col.append(highest_count)
    count_col.append(count)

# Cast dictionary into a Dataframe

final_target_df = pd.DataFrame(data=final_target_dict)

# Alphabetically sort cities column

# Create final csv file

print(final_target_dict)
'''