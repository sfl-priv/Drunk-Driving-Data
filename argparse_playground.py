import argparse
import pandas as pd
from superfluous_city_list import cities
from get_master_files import concat_fars_ext
import os

# Define CLI functionality
parser = argparse.ArgumentParser(description='Data point to get counts for')
parser.add_argument('-c','--column', metavar='column', type=str, help='Picks a column in the dataset to get counts for')
parser.add_argument('-f', '--filename', metavar='filename', type=str, help='Picks which file from the FARS datasets to select')
args = parser.parse_args()
column = args.column
filename = args.filename


# Get master files and filter them to the columns we want
accident_file = pd.read_csv(concat_fars_ext(args.filename))
print("Created accident file")
person_file = pd.read_csv(concat_fars_ext(args.filename))
print("Created person file")

print(accident_file, person_file)

pd.read_csv(concat_fars_ext('accident.csv'))