from get_dui_deaths import person_file
from get_master_files import concat_fars_ext
from get_deaths_as_percentage import accident_file
import pandas as pd


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


# Create pivot table to show most common DUI car per city

dangerous_cars = final_truncated_list['MAK_MODNAME'].value_counts()
dangerous_cars.index[0]
dangerous_cars.iloc[0]

# Create for loop to do it for each city in the dataset

# Show columns in dataset

merge_cols = accident_file.keys()
columns = []
for column in merge_cols:
    columns.append(column)
print(columns)

# Show all values in a column

values = []
for value in set(final_truncated_list['CITYNAME']):
    values.append(value)
print(values)

print(len(set(final_truncated_list['MAK_MODNAME'])))

# Import list of cities from other file

cities_file = pd.read_csv("States and Cities.csv")
cities_file = cities_file['City']
print(list(cities_file))


city_spec_list = final_truncated_list[final_truncated_list.CITYNAME == 'LOS ANGELES']
dangerous_cars = city_spec_list['MAK_MODNAME'].value_counts()
print(dangerous_cars)




# Create a spreadsheet with the most common cars and how often they occur by each city in seed list

# Access 
cities_file = pd.read_csv("States and Cities.csv")

final_list = {
    'City' : [],
    'Most Common Car' : [],
    'Occurence Count' : []
}


for city in cities_file:
    city_spec_list = final_truncated_list[final_truncated_list.CITYNAME == f'{city}']
    if city not in cities_file:
        print(f"No data found for {city}, trying next one")
        continue
    else:
        dangerous_cars = city_spec_list['MAK_MODNAME'].value_counts()
        most_common_car = dangerous_cars.index[0]
        car_occurence_count = dangerous_cars.iloc[0]
        
final_file = pd.DataFrame(data=final_list)