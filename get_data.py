import os
import datetime
import pandas as pd
from pandas_datareader import wb
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
        indicators = [
            "EN.ATM.GHGT.KT.CE", # Total greenhouse gases in CO2
            "EG.ELC.RNEW.ZS", # Renewable energy in %
            "NY.GDP.MKTP.CD", # GDP in USD
            "NY.GDP.PCAP.CD", # GDP per capita in USD
            "NY.GDP.PCAP.PP.CD", # GDP per capita in PPP
            "NY.GDP.PCAP.KD.ZG", # GDP per capita growth in %
            "SP.POP.TOTL", # Total population
        ]
    if end_year == None:
        end_year = int(datetime.datetime.now().date().strftime("%Y"))

    # Check existing metadata
    appending = 0
    if os.path.exists("wb_metadata"):
        print("Metadata file found.")
        with open("wb_metadata") as f:
            metadata_parameters = f.read().split()
        if set(indicators) == set(metadata_parameters[:-2]):
            if int(metadata_parameters[-1]) < end_year:
                appending = 1
                start_year = int(metadata_parameters[-1]) + 1
            elif int(metadata_parameters[-2]) > start_year:
                appending = 1
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
        f.write(f"{start_year}\n")
        f.write(f"{end_year}\n")


if __name__ == "__main__":
    get_data()
