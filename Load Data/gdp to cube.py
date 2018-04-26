"""
Read US GDP data from FRED (Federal Reserve of St. Louis data) through quandl and push it to the Econ Cube

Run sample setup.py before running this script, to create the required cubes and dimensions!

Assumption: 
- quandl is installed

"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

# type 'pip install quandl' into cmd if you don't have quandl installed
import quandl
import math
from TM1py.Services import TM1Service

raw_data = quandl.get("FRED/GDP")

# create cellset and push it to Econ Cube
cellset = {}
for tmstp, row_data in raw_data.iterrows():
    # time mapping: YYYY-MM-DD to YYYY and QQ
    year = tmstp.year
    quarter = 'Q' + str(math.ceil(tmstp.month/3.))
    coordinates = ('USA', year, quarter, 'GDP')
    value = row_data.values[0]
    cellset[coordinates] = value

with TM1Service(**config['tm1srv01']) as tm1:
    tm1.cubes.cells.write_values('TM1py Econ', cellset)



