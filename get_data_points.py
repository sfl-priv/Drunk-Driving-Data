import pandas as pd
import os
import get_master_files as gf

# Filepath in: 
# /Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Downloads/Amanda Demanda - Drunk Driving Capitals/NHTSA FARS Data
# Filepath out: 
# /Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data

person_files = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Master Person File.csv")
person_files

print(gf.concat_fars_ext("person.csv"))

accident_file = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Master Accidents.csv")
person_file = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Master Person File.csv")
commuter_cities = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Downloads/Combined Datasets/Commuter Vehicles by city.csv")

# Get drunk driving fatalities per city
# Get drunk driving fatalities as percentage of total fatalities
# Get car most involved in drunk driving
# Get time which DUIs are most likely to happen


person_cols = person_file.keys()
columns = []
for column in person_cols:
    columns.append(column)
print(columns)


person_selected_cols = person_file[['STATENAME', 'ST_CASE', 'DAY', 'HOUR', 'ALC_STATUSNAME', 'DRINKING', ]]
print(person_selected_cols)

print(person_file[['DEVTYPENAME']])