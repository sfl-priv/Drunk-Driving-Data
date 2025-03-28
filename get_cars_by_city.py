import pandas as pd
import csv


# Read in the FARS file created in get_dangerous_cars.py file
file = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Final Truncated List.csv")

# Get all cities in a list
states_and_cities_csv = pd.read_csv("States and Cities.csv")
cities_only = states_and_cities_csv['City']
cities_only.tolist()

# Get all unique states in a set
states_only = states_and_cities_csv['State']
states_only.tolist()
unique_states = set(states_only)

def main():

    '''
    
    Find the cars that have been the most involved in drunk driving accidents for a list of cities.
    
    Based on the datasets in the NHTSA FARS downloads.
    
    '''

    # Declare final spreadsheet columns as empty lists
    cities_col = []
    car_col = []
    car_col_2 = []
    count_col = []
    count_col_2 = []

    # Prepare dataframe as empty dict with above lists as values
    final_target_dict = {
        'City' : cities_col,
        'Most Common Car' : car_col,
        'Second Most Common Car' : car_col_2,
        'Occurence Count' : count_col,
        'Occurence Count 2' : count_col_2,
    }
        
    # Filter master file only to target states where our cities are
    state_filtered_file = file[(file["STATENAME_x"].isin(unique_states))]
    
    # Iterate over the list of cities we want the cars for
    for city in cities_only:
        one_city_df = state_filtered_file[state_filtered_file.CITYNAME == f'{city}'] # Filter Dataframe to target city
        cities_col.append(f'{city}') # Add city name as spreadsheet column
        most_common_cars = one_city_df['MAK_MODNAME'].value_counts() # Find out how often a car's name occurs in the make and model column
        most_common_car_1 = most_common_cars.index[0] # Get the one that occurs the most
        most_common_car_2 = most_common_cars.index[1] # Get second most common car, in case the highest count is an unknown model
        most_common_count_1 = most_common_cars.iloc[0] # Get how often the most common car occurs
        most_common_count_2 = most_common_cars.iloc[1] # Get how often the second most common car occurs
        
        # Add all the extracted data to the lists which will contain our dictionary values
        car_col.append(most_common_car_1)
        car_col_2.append(most_common_car_2)
        count_col.append(most_common_count_1)
        count_col_2.append(most_common_count_2)
    
    # Convert dictionary to Dataframe object
    final_target_df = pd.DataFrame(data=final_target_dict)
    
    # Choose name and location for final spreadsheet
    filepath_out = input("File Save Location: ")
    filename_out = input("File Name: ")
    final_target_df.to_csv(f"{filepath_out}/{filename_out}.csv")


if __name__ == "__main__":
    main()