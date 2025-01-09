import pandas as pd
import requests

#Retrieve all accidents for five years with their case ID as well as state and city
years = [2018, 2019, 2020, 2021, 2022]
first_time = True
for year in years:
    #Create the container with the first year
	accident_file = f"/Users/sebastianfirrell/Desktop/Impaired, Distracted, or Intoxicated Driving/{year}/All Accidents.csv"
	if first_time == True:
		accident_master_container = pd.read_csv(accident_file, encoding='unicode_escape', usecols=['STATENAME', 'ST_CASE', 'CITYNAME'])
		first_time = False
	else:
     #Append all the others to it
		single_year_accident = pd.read_csv(accident_file, encoding='unicode_escape', usecols=['STATENAME', 'ST_CASE', 'CITYNAME'])
		accident_master_container = pd.concat([accident_master_container, single_year_accident], ignore_index=True)
  
print(accident_master_container)

#Retrieve all accidents for five years with their case ID as well as state and city
years = [2018, 2019, 2020, 2021, 2022]
first_time = True
for year in years:
    #Create the container with the first year
	distracted_file = f"/Users/sebastianfirrell/Desktop/Impaired, Distracted, or Intoxicated Driving/{year}/Distracted Driving Accidents.csv"
	if first_time == True:
		distracted_master_container = pd.read_csv(distracted_file, encoding='unicode_escape', usecols=['ST_CASE', 'MDRDSTRDNAME'])
		first_time = False
	else:
     #Append all the others to it
		single_year_distracted = pd.read_csv(distracted_file, encoding='unicode_escape', usecols=['ST_CASE', 'MDRDSTRDNAME'])
		distracted_master_container = pd.concat([distracted_master_container, single_year_distracted], ignore_index=True)

print(distracted_master_container)

years = [2018, 2019, 2020, 2021, 2022]
first_time = True
for year in years:
    #Create the container with the first year
	impaired_file = f"/Users/sebastianfirrell/Desktop/Impaired, Distracted, or Intoxicated Driving/{year}/Impaired Driving Accidents.csv"
	if first_time == True:
		impaired_master_container = pd.read_csv(impaired_file, encoding='unicode_escape', usecols=['ST_CASE', 'DRIMPAIRNAME'])
		first_time = False
	else:
     #Append all the others to it
		single_year_impaired = pd.read_csv(impaired_file, encoding='unicode_escape', usecols=['ST_CASE', 'DRIMPAIRNAME'])
		impaired_master_container = pd.concat([impaired_master_container, single_year_impaired], ignore_index=True)

print(impaired_master_container)

years = [2018, 2019, 2020, 2021, 2022]
first_time = True
for year in years:
    #Create the container with the first year
	intoxicated_file = f"/Users/sebastianfirrell/Desktop/Impaired, Distracted, or Intoxicated Driving/{year}/Intoxicated Driving Accidents.csv"
	if first_time == True:
		intoxicated_master_container = pd.read_csv(intoxicated_file, encoding='unicode_escape', usecols=['ST_CASE', 'DRUGRESNAME'])
		first_time = False
	else:
     #Append all the others to it
		single_year_intoxicated = pd.read_csv(intoxicated_file, encoding='unicode_escape', usecols=['ST_CASE', 'DRUGRESNAME'])
		intoxicated_master_container = pd.concat([intoxicated_master_container, single_year_intoxicated], ignore_index=True)

print(intoxicated_master_container)

#Perform database merge of all dataframes into a single dataframe