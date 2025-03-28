from get_dui_deaths import person_file
from get_master_files import concat_fars_ext
from get_deaths_as_percentage import accident_file
import pandas as pd


def get_working_sheet():
    # Get full file for all five years
    vehicle_file = concat_fars_ext("vehicle.csv")
    vehicle_file = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Master Vehicle File.csv")

    # Merge vehicle file with accident file and then with the person file
    vehicle_merge = pd.merge(accident_file, vehicle_file, on=['ST_CASE'])
    vehicle_merge.to_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Vehicle_merge_file.csv")

    # Select columns in vehicle merge to reduce file size
    truncated_vehicle_merge = vehicle_merge[['ST_CASE', 'MAK_MODNAME', 'CITYNAME', 'STATENAME_x']]
    truncated_vehicle_merge.to_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Truncated Vehicle Merge.csv")

    # Filter person file only to case and drinking deaths
    truncated_person_file = person_file[['ST_CASE', 'DRINKINGNAME', 'DRINKING']]
    
    # Merge both truncated datasets into a final file
    final_truncated_list = pd.merge(truncated_vehicle_merge, truncated_person_file, on=['ST_CASE'])

    # Select columns only showing cars and where a DUI death occured
    final_truncated_list = final_truncated_list[final_truncated_list.CITYNAME != 'NOT APPLICABLE']
    final_truncated_list = final_truncated_list[final_truncated_list.CITYNAME != 'Other']
    final_truncated_list = final_truncated_list[final_truncated_list.DRINKINGNAME == 'Yes (Alcohol Involved)']
    final_truncated_list.to_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Final Truncated List.csv")

    # Show all values in a column
    values = []
    column = input("Column: ")
    for value in set(final_truncated_list[column]):
        values.append(value)
    print(values)
    print(len(set(final_truncated_list['MAK_MODNAME'])))