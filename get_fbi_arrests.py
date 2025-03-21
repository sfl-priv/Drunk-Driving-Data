import requests
import pandas as pd
import time
from datetime import datetime
import matplotlib.pyplot as plt

# API details
FBI_API_KEY = "y1fxpEZRHEzCjNHbGrup3Y1wRQ6gf64grLBNb8P4"  # Replace with your API key
BASE_URL = "https://api.usa.gov/crime/fbi/cde/arrest/agencies/"

# List of 10 major US cities with their ORI codes
# ORI codes are unique identifiers for law enforcement agencies
cities = {
    "New York": "NY0310000",
    "Los Angeles": "CA0194200",
    "Chicago": "IL0160400",
    "Houston": "TX1010100",
    "Phoenix": "AZ0072100",
    "Philadelphia": "PA0510100",
    "San Antonio": "TX0150100",
    "San Diego": "CA0371100",
    "Dallas": "TX0570100",
    "San Jose": "CA0431000"
}

# Years to collect data for
years = list(range(2019, 2024))  # 2019-2023

# Function to get DUI arrest data for a specific city and year
def get_dui_arrests(ori, year):
    url = f"{BASE_URL}/{ori}/dui"
    
    params = {
        "from": f"{year}-01-01",
        "to": f"{year}-12-31",
        "api_key": FBI_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract DUI arrest count
        if "results" in data and data["results"]:
            return data["results"][0]["data"]["Drunkenness"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {ori}, year {year}: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Data format error for {ori}, year {year}: {e}")
        return None

# Create a DataFrame to store results
results = pd.DataFrame(index=cities.keys(), columns=[str(year) for year in years])

# Collect data for each city and year
for city_name, ori in cities.items():
    print(f"Collecting data for {city_name}...")
    for year in years:
        arrests = get_dui_arrests(ori, year)
        results.loc[city_name, str(year)] = arrests
        time.sleep(1)  # Rate limiting to avoid API throttling

# Save results to CSV
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"dui_arrests_{timestamp}.csv"
results.to_csv(csv_filename)
print(f"Data saved to {csv_filename}")

# Convert data to numeric for visualization
results_numeric = results.apply(pd.to_numeric, errors='coerce')

# Create a bar chart
plt.figure(figsize=(14, 8))
ax = results_numeric.T.plot(kind='bar')
plt.title('DUI Arrests by City (2019-2023)')
plt.xlabel('Year')
plt.ylabel('Number of Arrests')
plt.xticks(rotation=45)
plt.legend(title='City', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Save the chart
chart_filename = f"dui_arrests_chart_{timestamp}.png"
plt.savefig(chart_filename)
print(f"Chart saved to {chart_filename}")

# Show the results
print("\nDUI Arrest Data (2019-2023):")
print(results)