import argparse
import pandas as pd
from superfluous_city_list import cities
from get_master_files import concat_fars_ext

# Enable CLI args to choose data
parser = argparse.ArgumentParser(description='Data point to get counts for')
parser.add_argument('-c','--column', metavar='column', type=str, help='Picks a column in the dataset to get counts for')
parser.add_argument('-f', '--filename', metavar='filename', type=str, help='Picks which file from the FARS datasets to select')
args = parser.parse_args()
column = args.column
filename = args.filename



def main():


    # Get master files and filter them to the columns we want
    accident_file = pd.read_csv(concat_fars_ext(args.filename), usecols=['ST_CASE', 'TWAY_ID', 'STATENAME', 'CITYNAME'])
    person_file = pd.read_csv(concat_fars_ext(args.filename), usecols=['ST_CASE', 'DRINKING', 'DRINKINGNAME'])
    
    # Merge person and accident files
    merged_file = pd.merge(accident_file, person_file, on=['ST_CASE'])
    
    # Get all cities in a list if we need them
    states_and_cities_csv = pd.read_csv("States and Cities.csv")
    cities_only = states_and_cities_csv['City']
    cities_only.tolist()

    # Get all unique states in a set
    states_only = states_and_cities_csv['State']
    states_only.tolist()
    unique_states = set(states_only)


    # Declare final spreadsheet columns as empty lists
    cities_col = []
    street_col = []
    count_col = []

    # Prepare dataframe as empty dict with above lists as values
    final_target_dict = {
        'City' : cities_col,
        'Most Common Street' : street_col,
        'Occurence Count' : count_col,
    }
        
    # Filter master file only to target states where our cities are
    state_filtered_file = merged_file[(merged_file["STATENAME_x"].isin(unique_states))]



if __name__ == "__main__":
    main()