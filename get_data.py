from pandas_datareader import wb
from tqdm import tqdm
import datetime


def get_data():
    """
    The function to get data from World Bank and convert into an CSV file.
    """
    indicators = [
        "EN.ATM.GHGT.KT.CE", # Total greenhouse gases in CO2
        "EG.ELC.RNEW.ZS", # Renewable energy in %
        "NY.GDP.MKTP.CD", # GDP in USD
        "NY.GDP.PCAP.CD", # GDP per capita in USD
        "NY.GDP.PCAP.PP.CD", # GDP per capita in PPP
        "NY.GDP.PCAP.KD.ZG", # GDP per capita growth in %
        "SP.POP.TOTL", # Total population
    ]
    start_year = 2000
    end_year = int(datetime.datetime.now().date().strftime("%Y"))
    data = wb.download(
        indicator=indicators,
        country="all",
        start=start_year,
        end=end_year
    )
    data.to_csv("wb_data.csv")


if __name__ == "__main__":
    get_data()
