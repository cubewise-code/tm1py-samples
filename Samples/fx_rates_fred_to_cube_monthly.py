"""
Read FX data from FRED (Federal Reserve of St. Louis data) through pandas and push it to the fx cube
Prerequisites:
1. Create the required cubes and dimensions
    Run TM1py sample Load Data\samples setup.py
2. Install pandas
    type 'pip install pandas' into cmd if you don't have pandas installed
3. Add pandas_reader module:
    To install it, run in command line: pip install pandas_datareader
"""
import collections
import configparser
from datetime import datetime

# type 'pip install pandas_datareader' into cmd if you don't have pandas_datareader installed
import pandas_datareader.data as web
from TM1py.Services import TM1Service

config = configparser.ConfigParser()
config.read(r'..\config.ini')

cube_name = 'TM1py FX Rates Monthly'
currency_pairs = {
    'EXUSAL': {'From': 'USD', 'To': 'AUD', 'Invert': 'N'},
    'EXUSUK': {'From': 'USD', 'To': 'GBP', 'Invert': 'N'},
    'EXUSEU': {'From': 'USD', 'To': 'EUR', 'Invert': 'N'},
    'EXHKUS': {'From': 'USD', 'To': 'HKD', 'Invert': 'Y'},
    'EXSIUS': {'From': 'USD', 'To': 'SGD', 'Invert': 'Y'},
    'EXSZUS': {'From': 'USD', 'To': 'CHF', 'Invert': 'Y'},
    'EXCHUS': {'From': 'USD', 'To': 'RMB', 'Invert': 'Y'},
    'EXTAUS': {'From': 'USD', 'To': 'TWD', 'Invert': 'Y'},
    'EXINUS': {'From': 'USD', 'To': 'INR', 'Invert': 'Y'},
    'EXJPUS': {'From': 'USD', 'To': 'JPY', 'Invert': 'Y'}
}

for currency_ticker, currency_details in currency_pairs.items():

    # Load FX Rates from FRED through pandas datareader
    start = datetime(year=2016, month=1, day=1)
    raw_data = web.get_data_fred(currency_ticker, start)

    # Remove NaN
    data = raw_data.dropna()

    # Create cellset and push it to FX Cube
    cellset = collections.OrderedDict()
    for tmstp, data in data.iterrows():
        date = tmstp.date()
        my_year, my_month = date.year, date.month
        # Handle Australian Financial Year
        if my_month > 6:
            my_year += 1
        # Handle Inverted FX Rates
        if currency_details["Invert"] == 'Y':
            value = 1 / data.values[0]
        else:
            value = data.values[0]
        coordinates = (currency_details["From"], currency_details["To"], my_year, my_month, 'Month Close')
        cellset[coordinates] = value
    with TM1Service(**config['tm1srv01']) as tm1:
        tm1.cubes.cells.write_values(cube_name, cellset)
