"""
Read FX data from FRED (Federal Reserve of St. Louis data) through pandas and push it to the fx cube

Prerequisites:
1. Create the required cubes and dimensions
    Run TM1py sample Load Data\sample setup.py
2. Install pandas
    type 'pip install pandas' into cmd if you don't have pandas installed
3. Add pandas_reader module:
    To install it, run in command line: pip install pandas_datareader

"""
import configparser
from datetime import datetime

# type 'pip install pandas_datareader' into cmd if you don't have pandas_datareader installed
import pandas_datareader.data as web
from TM1py.Services import TM1Service

config = configparser.ConfigParser()
config.read(r'..\config.ini')

# FX Cube Name
cube_name = 'TM1py FX Rates'

# FRED Tickers with properties
# https://fred.stlouisfed.org/series/DEXUSEU
currency_pairs = {
    'DEXUSAL': {'From': 'USD', 'To': 'AUD', 'Invert': 'N'},
    'DEXUSUK': {'From': 'USD', 'To': 'GBP', 'Invert': 'Y'},
    'DEXUSEU': {'From': 'USD', 'To': 'EUR', 'Invert': 'Y'},
    'DEXHKUS': {'From': 'USD', 'To': 'HKD', 'Invert': 'N'},
    'DEXSIUS': {'From': 'USD', 'To': 'SGD', 'Invert': 'N'},
    'DEXSZUS': {'From': 'USD', 'To': 'CHF', 'Invert': 'N'},
    'DEXCHUS': {'From': 'USD', 'To': 'RMB', 'Invert': 'N'},
    'DEXTAUS': {'From': 'USD', 'To': 'TWD', 'Invert': 'N'},
    'DEXINUS': {'From': 'USD', 'To': 'INR', 'Invert': 'N'},
    'DEXJPUS': {'From': 'USD', 'To': 'JPY', 'Invert': 'N'}
}

# Container to store data that we write to TM1 in the end (in one batch)
cellset = dict()

for currency_ticker, currency_details in currency_pairs.items():
    # load FX Rates for USD to JPY from FRED through pandas datareader
    start = datetime(year=2016, month=1, day=1)
    raw_data = web.get_data_fred(currency_ticker, start)

    # Remove NaN
    data = raw_data.dropna()

    # Push values into cellset
    for tmstp, data in data.iterrows():
        date = tmstp.date()
        # Handle Inverted FX Rates
        if currency_details["Invert"] == 'Y':
            value = 1 / data.values[0]
        else:
            value = data.values[0]
        coordinates = (currency_details["From"], currency_details["To"], str(date), 'Spot')
        cellset[coordinates] = value

with TM1Service(**config['tm1srv01']) as tm1:
    tm1.cubes.cells.write_values(cube_name, cellset)
