import pandas as pd
import os
import sys

def main():
    target_file = input("Name of file to concatenate: ")
    accidents = concat_fars_ext(f"{target_file}.csv")
    print(accidents)
    


def concat_fars_ext(f): # Takes the file we want from FARS as sole argument
    need_the_data = True
    years = [2018, 2019, 2020, 2021, 2022]
    filepath_in = input("Folder Location: ")
    os.chdir(f"{filepath_in}")
    filename_in = f
    filepath_out= input("Filepath out: ")
    filename_out = input("Output File Name: ")
    if need_the_data:
    # For the first time around, create the dataframe
        i = True
        for year in years:
            file = f"./{year}/{filename_in}"
            if i:
                master_file_df = pd.read_csv(file, encoding='unicode_escape')
                master_file_df['Year'] = year
                i = False
            # For the subsequenet times around, just append the new years data to the dataframe
            else:
                single_year_file_df = pd.read_csv(file, encoding='unicode_escape')
                single_year_file_df['Year'] = year
                master_file_df = pd.concat([master_file_df, single_year_file_df], ignore_index=True)
                master_file_df.to_csv(f"{filepath_out}/{filename_out}.csv", index=False)
                return (f"{filepath_out}/{filename_out}.csv")
            

if __name__ == "__main__":
    main()