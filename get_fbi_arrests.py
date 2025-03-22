import requests
import pandas as pd

key = "y1fxpEZRHEzCjNHbGrup3Y1wRQ6gf64grLBNb8P4"

#Import list of all cities we want to check
seed_list = pd.read_csv("/Users/sebastianfirrell/Desktop/DPR Data Analysis/Data Code/Amanda Demanda - Drunk Driving Hotspots Code/States and Cities.csv")

base_url = "https://api.usa.gov/crime/fbi/cde"
url = f"{base_url}/AK?API_KEY={key}"

#Check the endpoint connection is successful
response = requests.get(url)
if response == "200":
    print("Request Successful")
else:
    print(f"Error: {response}")
    
# def get_seed_list_city():
    
# def get_fbi_info():
    
# def main():
    
if __name__ == "__main__":
    main()