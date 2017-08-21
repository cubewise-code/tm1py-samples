"""
Read US GDP data from FRED (Federal Reserve of St. Louis data) through quandl and push it to the Econ Cube

Assumption: 
- 'Econ' Cube exists with 3 Dimensions: Country, Year, Quarter, Econ Measure
- quandl is installed

"""

# type 'pip install quandl' into cmd if you don't have quandl installed
import quandl
from TM1py.Services import TM1Service


raw_data = quandl.get("FRED/GDP")

# create cellset and push it to Econ Cube
cellset = {}
for tmstp, row_data in raw_data.iterrows():
    # time mapping: YYYY-MM-DD to YYYY and QQ
    year = tmstp.year
    quarter = 'Q' + str(tmstp.month//4 + 1)
    coordinates = ('USA', year, quarter, 'GDP')
    value = row_data.values[0]
    cellset[coordinates] = value

with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:
    tm1.data.write_values('Econ', cellset)



