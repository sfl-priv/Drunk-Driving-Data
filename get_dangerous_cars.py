from get_dui_deaths import person_file
from get_master_files import concat_fars_ext
from get_deaths_as_percentage import accident_file
import pandas as pd



def get_working_sheet():
    # Get full file for all five years
    vehicle_file = concat_fars_ext("vehicle.csv")
    vehicle_file = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Master Vehicle File.csv")
    accident_file
    vehicle_file

    # Merge vehicle file with accident file and then with the person file

    vehicle_merge = pd.merge(accident_file, vehicle_file, on=['ST_CASE'])
    vehicle_merge.to_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Vehicle_merge_file.csv")

    # Select columns in vehicle merge to reduce file size

    truncated_vehicle_merge = vehicle_merge[['ST_CASE', 'MAK_MODNAME', 'CITYNAME', 'STATENAME_x']]
    truncated_vehicle_merge.to_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Truncated Vehicle Merge.csv")

    # Filter person file only to case and drinking deaths

    truncated_person_file = person_file[['ST_CASE', 'DRINKINGNAME', 'DRINKING']]
    truncated_person_file

    # Merge both truncated datasets into a final file

    final_truncated_list = pd.merge(truncated_vehicle_merge, truncated_person_file, on=['ST_CASE'])
    final_truncated_list

    # Select columns only showing cars and where a DUI death occured

    final_truncated_list = final_truncated_list[final_truncated_list.CITYNAME != 'NOT APPLICABLE']
    final_truncated_list = final_truncated_list[final_truncated_list.CITYNAME != 'Other']
    final_truncated_list = final_truncated_list[final_truncated_list.DRINKINGNAME == 'Yes (Alcohol Involved)']
    final_truncated_list.to_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Final Truncated List.csv")


def get_values():
    # Show all values in a column
    values = []
    column = input("Column: ")
    for value in set(final_truncated_list[column]):
        values.append(value)
    print(values)
    print(len(set(final_truncated_list['MAK_MODNAME'])))

def testing():
    
    """Testing why it doesn't work"""
    
    # Get Master File
    final_truncated_list = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Final Truncated List.csv")
        
    # Declare soreadsheet columns as empty lists
    test_cities_col = []
    test_car_col = []
    test_car_col_2 = []
    test_occurence_col = []
    test_occurence_col_2 = []

    # Test lists for columns for this exercise
    test_state_list = ['California', 'Arizona', 'Tennessee', 'Nebraska', 'Arizona', 'North Carolina']
    test_city_list = ['LOS ANGELES', 'PHOENIX', 'NASHVILLE', 'OMAHA', 'TUCSON', 'TUCSON']


    # Try state and city as dict
    
    state_city_pair = {
        'State' : ['California', 'Arizona', 'Tennessee', 'Nebraska', 'Arizona', 'North Carolina'],
        'City' : ['LOS ANGELES', 'PHOENIX', 'NASHVILLE', 'OMAHA', 'TUCSON', 'TUCSON']
    }
    
    cap_cities = []
    for city in state_city_pair.get('City'):
        city = city.upper()
        cap_cities.append(city)
        print(cap_cities)
        
    # Empty spreadsheet with th ecolumns we want
    test_final_dict = {
        'City' : test_cities_col,
        'Most Common Car' : test_car_col,
        'Second Most Common Car' : test_car_col_2,
        'Occurence Count' : test_occurence_col,
        'Occurence Count 2' : test_occurence_col_2,
        'State' : test_state_list
    }


    # Iterate over test lists
    for city in cap_cities:
        if city not in test_city_list: # Skip if city not found
            print(f"No data found for {city}, trying next one")
            pass
        else:
            city_specific_table = final_truncated_list[final_truncated_list.CITYNAME == f'{city}'] # Filter dataframe for selected city only
            test_cities_col.append(f'{city}') # Add city row to spreadsheet
            dangerous_cars = city_specific_table['MAK_MODNAME'].value_counts() # Find table of most occuring values in MAK_MODNAME column
            most_common_car = dangerous_cars.index[0] # Pick top row of table
            second_most_common_car = dangerous_cars.index[1] # Pick second row
            car_occurence_count = dangerous_cars.iloc[0] # Fetch how often it occured
            car_occurence_count_2 = dangerous_cars.iloc[1]
            test_car_col.append(most_common_car) # Put car name in same row
            test_car_col_2.append(second_most_common_car)
            test_occurence_col.append(car_occurence_count) # Put occurence count in same row
            test_occurence_col_2.append(car_occurence_count_2)
    
    test_df = pd.DataFrame(data=test_final_dict)
    test_df


def final_function():
    
    '''Create a spreadsheet with the most common cars and how often they occur by each city in seed list'''

    # Get Master file    
    final_truncated_list = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Final Truncated List.csv")

    
    # Import list of cities from other file
    cities_file = pd.read_csv("States and Cities.csv")
    cities_file = cities_file['City']
    
    # Declare final spreadsheet columns as empty lists
    cities_col = []
    car_col = []
    car_col_2 = []
    count_col = []
    count_col_2 = []

    # Prepare dataframe as empty dict with above lists as values
    final_spreadsheet = {
        'City' : cities_col,
        'Most Common Car' : car_col,
        'Second Most Common Car' : car_col_2,
        'Occurence Count' : count_col,
        'Occurence Count 2' : count_col_2,
    }
    
    # Put city names from csv in all caps
    cap_cities = []
    for city in cities_file:
        city = city.upper()
        cap_cities.append(city)
        
    print(cap_cities)

    
    for city in cap_cities:
        if city not in cap_cities: # Skip if city not found
            print(f"No data found for {city}, trying next one")
            pass
        else:
            city_spec_list = final_truncated_list[final_truncated_list.CITYNAME == f'{city}'] # Filter dataframe for selected city only
            cities_col.append(f'{city}')
            dangerous_cars = city_spec_list['MAK_MODNAME'].value_counts() # Find most occuring values in MAK_MODNAME column
            most_common_car = dangerous_cars.index[0]
            print(most_common_car)
            second_most_common_car = dangerous_cars.index[1] 
            car_occurence_count = dangerous_cars.iloc[0] # Fetch how often it recurred
            car_occurence_count_2 = dangerous_cars.iloc[1]
            car_col.append(most_common_car)
            car_col_2.append(second_most_common_car)
            count_col.append(car_occurence_count)
            count_col_2.append(car_occurence_count_2)
            
    
    print(final_spreadsheet)
    final_df = pd.DataFrame(data=final_spreadsheet)
    final_df
    
    fort_worth = final_truncated_list[final_truncated_list.CITYNAME == 'SEATTLE'] # Filter dataframe for selected city only
    fort_worth_count = fort_worth['MAK_MODNAME'].value_counts() # Find most occuring values in MAK_MODNAME column
    print(fort_worth_count.index[0], fort_worth_count.iloc[0])

