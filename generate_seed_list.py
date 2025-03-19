import requests
import pandas as pd
import json

key = "c6626ccdcb7542e94909cec187af575af3fc4693"

response = requests.get(f"https://api.census.gov/data/2021/pep/natmonthly?get=POP,NAME,MONTHLY&for=us:*&MONTHLY=4&key={key}")
data = response.json()
print(data)



dataframe = pd.read_json(f"https://api.census.gov/data/2021/pep/natmonthly?get=POP&for=GEO_ID&key={key}")
print(dataframe)