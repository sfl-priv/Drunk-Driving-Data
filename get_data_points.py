import pandas as pd
import os
import get_master_files as gf

# Read in all spreadsheets
person_file = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Master Person File.csv", low_memory=False)
accident_file = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Master Accidents.csv", low_memory=False)
seed_list = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Downloads/Combined Datasets/Commuter Vehicles by city_with_population.csv", low_memory=False)

# Get drunk driving fatalities per city
# Get drunk driving fatalities as percentage of total fatalities
# Get car most involved in drunk driving
# Get time which DUIs are most likely to happen


'''
Merge both sheets on ST_CASE
'''
drunk_driving_merge = accident_file.merge(person_file, on='ST_CASE')



'''
Print all columns in dataset
'''
merge_cols = drunk_driving_merge.keys()
columns = []
for column in merge_cols:
    columns.append(column)
print(columns)



'''
Filter columns for only crashes in cities and those that involve drinking
'''

drunk_driving_new_cols = drunk_driving_merge[['DRINKING', 'CITYNAME', 'STATENAME_x', 'DRINKINGNAME']]
drunk_driving_new_cols = drunk_driving_new_cols[drunk_driving_merge.CITYNAME != 'NOT APPLICABLE']
drunk_driving_new_cols = drunk_driving_new_cols[drunk_driving_merge.CITYNAME != 'Other']
drunk_driving_new_cols = drunk_driving_new_cols[drunk_driving_new_cols.DRINKINGNAME == 'Yes (Alcohol Involved)']


'''
Get highest drinking death counts by city
'''

# Group by CITYNAME and count the DRINKING column
drinking_by_city = drunk_driving_new_cols.groupby('CITYNAME')['DRINKING'].count().reset_index()

# Rename the count column to something more descriptive
drinking_by_city = drinking_by_city.rename(columns={'DRINKING': 'DRINKING_COUNT'})

# Sort values by the count in descending order
drinking_by_city = drinking_by_city.sort_values('DRINKING_COUNT', ascending=False)

drinking_by_city.to_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Drunk Driving Deaths by City.csv")
