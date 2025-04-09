import pandas as pd
import argparse

parser = argparse.ArgumentParser(prog='Return a Value Counts Spreadsheet', description='Data point to get counts for')
parser.add_argument('-c','--column', metavar='column', type=str, help='Picks a column in the dataset to get counts for')
args = parser.parse_args()
column = args.column


def main():
    filepath_in = input("Select File: ")
    filepath_out = input("Where will the file go? ")
    filename_out = input("Final file nane: ")
    if "csv" not in filename_out:
        filename_out = f"{filename_out}.csv"
    file = pd.read_csv(filepath_in)
    counts = get_counts(file)
    counts.to_csv(f"{filepath_out}/{filename_out}")

def get_counts(file):
    counts = file[args.column].value_counts()
    return counts


if __name__ == "__main__":
    main()