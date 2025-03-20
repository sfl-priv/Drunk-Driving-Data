import pandas as pd
from get_dui_deaths import drunk_driving_merge

# Read in all spreadsheets
person_file = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Master Person File.csv", low_memory=False)
accident_file = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Master Accidents.csv", low_memory=False)
seed_list = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Downloads/Combined Datasets/Commuter Vehicles by city_with_population.csv", low_memory=False)


'''
Narrow down to all columns we want
'''
drunk_driving_new_cols = drunk_driving_merge[['DRINKING', 'CITYNAME', 'STATENAME_x', 'DRINKINGNAME']]
drunk_driving_new_cols = drunk_driving_new_cols[drunk_driving_merge.CITYNAME != 'NOT APPLICABLE']
drunk_driving_new_cols = drunk_driving_new_cols[drunk_driving_merge.CITYNAME != 'Other']

unique_vals = drunk_driving_merge['DRINKINGNAME'].unique()
unique_vals


'''
Get drinking incidents as proportion of total crashes
'''

# Calculate total crashes per city
total_crashes = drunk_driving_new_cols.groupby(['CITYNAME', 'STATENAME_x']).size().reset_index(name='Total_Crashes')

# Calculate drinking-related crashes per city (where DRINKING == 1)
drinking_crashes = drunk_driving_new_cols[drunk_driving_new_cols['DRINKING'] == 1].groupby(['CITYNAME', 'STATENAME_x']).size().reset_index(name='Drinking_Crashes')

# Merge the two dataframes
merged_df = pd.merge(total_crashes, drinking_crashes, on=['CITYNAME', 'STATENAME_x'], how='left')

# Replace NaN values with 0 (cities with no drinking-related crashes)
merged_df['Drinking_Crashes'] = merged_df['Drinking_Crashes'].fillna(0)

# Calculate percentage
merged_df['Percentage_Drinking_Crashes'] = (merged_df['Drinking_Crashes'] / merged_df['Total_Crashes'] * 100).round(2)

# Rename columns for clarity
result_df = merged_df.rename(columns={'CITYNAME': 'City', 'STATENAME_x': 'State'})

# Sort by percentage in descending order
result_df = result_df.sort_values('Percentage_Drinking_Crashes', ascending=False)

# Display the result
print(result_df)

result_df.to_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Exports/Amanda Demanda - Drunk Driving Capitals Data/Drunk Driving Incidents As Proportion of Total Incidents.csv")