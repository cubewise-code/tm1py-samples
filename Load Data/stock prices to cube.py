"""
Read IBM Stock data from Wiki through quandl and push it to the Stock cube

Run sample setup.py before running this script, to create the required cubes and dimensions!

Prerequisites:
1. Create the required cubes and dimensions
    Run TM1py sample Load Data\setup.py
2. Install quandl
    type 'pip install quandl' into cmd if you don't have quandl installed
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')
# type 'pip install quandl' into cmd if you don't have quandl installed
import quandl
from TM1py.Services import TM1Service

# load Stock data for IBM
data = quandl.get("WIKI/IBM", start_date='2015-01-01', end_date='2017-08-11')

# create cellset from raw data
cube = 'TM1py Stock Prices'
measures = ('Open', 'High', 'Low', 'Close', 'Volume', 'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume')
cellset = {}
for tmstp, row in data.iterrows():
    date = tmstp.date()
    for measure in measures:
        cellset[('IBM', str(date), measure)] = row[measure]

# push data to TM1
with TM1Service(**config['tm1srv01']) as tm1:
    tm1.cubes.cells.write_values(cube, cellset)

