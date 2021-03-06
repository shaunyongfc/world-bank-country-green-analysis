import os
import datetime
import pandas as pd
from pandas_datareader import wb
from EDA_utils import indicators_dict
# from tqdm import tqdm


def get_data(indicators=None, start_year=2000, end_year=None):
    """
    The function to get data from World Bank and convert into an CSV file.
    wb_metadata text file will also generated containing information about the CSV file.
    If wb_metadata exists, the function will check it and try to minimise the
    download required by just appending necessary data.

    indicators, start_year, end_year:
        Parameter to be passed into pandas_datareader.wb.download()

    Default Values
        - start_year: 2000
        - end_year: Current year
    """
    # Initialise parameters
    if indicators == None:
        indicators = list(indicators_dict.keys())
    if end_year == None:
        end_year = int(datetime.datetime.now().date().strftime("%Y"))

    meta_start_year = start_year
    meta_end_year = end_year

    # Check existing metadata
    appending = 0
    if os.path.exists("wb_metadata"):
        print("Metadata file found.")
        with open("wb_metadata") as f:
            metadata_parameters = f.read().split()
        if set(indicators) == set(metadata_parameters[:-2]):
            if int(metadata_parameters[-1]) < end_year:
                appending = 1
                meta_start_year = min(int(metadata_parameters[-2]), start_year)
                start_year = int(metadata_parameters[-1]) + 1
            elif int(metadata_parameters[-2]) > start_year:
                appending = 1
                meta_end_year = max(int(metadata_parameters[-1]), end_year)
                end_year = int(metadata_parameters[-2]) - 1
            else:
                print("Data is up to date.")
                return
        else:
            print("Indicators do not match.")

    # tqdm.pandas()
    # Been trying to get progress bar when downloading without murdering
    # the time efficiency, but no success

    # Download data
    data = wb.download(
        indicator=indicators,
        country="all",
        start=start_year,
        end=end_year
    )

    # Save into CSV
    if appending:
        data.to_csv("wb_data.csv", mode="a", header=False)
        print("Data updated.")
    else:
        data.to_csv("wb_data.csv")
        print("Data saved.")

    # Write metadata
    with open("wb_metadata", "w") as f:
        f.write("\n".join(indicators) + "\n")
        f.write(f"{meta_start_year}\n")
        f.write(f"{meta_end_year}\n")


if __name__ == "__main__":
    get_data()
