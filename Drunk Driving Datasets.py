import pandas as pd
import requests

#Retrieve all accidents for five years with their case ID as well as state and city
years = [2018, 2019, 2020, 2021, 2022]
first_time = True
for year in years:
    #Create the container with the first year
	accdident_file = f"/Users/sebastianfirrell/Desktop/Data Exports/Amanda Demanda - Deadliest Roads in Texas/NHTSA FARS Data/{year}/accident.csv"
	if first_time == True:
		accident_master_container = pd.read_csv(accdident_file, encoding='unicode_escape', usecols=['STATENAME', 'ST_CASE', 'CITYNAME'])
		first_time = False
	else:
     #Append all the others to it
		single_year_accident = pd.read_csv(accdident_file, encoding='unicode_escape', usecols=['STATENAME', 'ST_CASE', 'CITYNAME'])
		accident_master_container = pd.concat([accident_master_container, single_year_accident], ignore_index=True)
  
print(accident_master_container)

