"""
Create all cubes and dimensions thar are required for the Load Data Samples:
- fx rates to cube
- gdp to cube
- stock prices to cube
"""

from TM1py.Objects import Cube, Dimension, Hierarchy, Element
from TM1py.Services import TM1Service

from datetime import timedelta, date


# Time magic with python generator
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


# push data to TM1
with TM1Service(address="", port="8001", user="admin", password="apple", ssl=True) as tm1:
    # create stuff for fx rates sample
    currencies = ('EUR', 'JPY', 'CHF', 'USD', 'AUD')
    elements = [Element(e, 'Numeric') for e in currencies]

    hierarchy = Hierarchy('TM1py Currency From', 'TM1py Currency From', elements)
    dimension = Dimension('TM1py Currency From', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    hierarchy = Hierarchy('TM1py Currency To', 'TM1py Currency To', elements)
    dimension = Dimension('TM1py Currency To', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    start_date = date(1940, 1, 1)
    end_date = date(2041, 1, 1)
    elements = [Element(str(single_date), 'Numeric') for single_date in daterange(start_date, end_date)]
    hierarchy = Hierarchy('TM1py Date', 'TM1py Date', elements)
    dimension = Dimension('TM1py Date', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    elements = [Element('Spot', 'Numeric')]
    hierarchy = Hierarchy('TM1py FX Rates Measure', 'TM1py FX Rates Measure', elements)
    dimension = Dimension('TM1py FX Rates Measure', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    cube = Cube('TM1py FX Rates', ['TM1py Currency From', 'TM1py Currency To', 'TM1py Date', 'TM1py FX Rates Measure'])
    if not tm1.cubes.exists(cube.name):
        tm1.cubes.create(cube)

    # create stuff for gdp sample
    countries = ('USA', 'AUS', 'DEU')
    elements = [Element(country, 'Numeric') for country in countries]
    hierarchy = Hierarchy('TM1py Country', 'TM1py Country', elements)
    dimension = Dimension('TM1py Country', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    elements = [Element(str(year), 'Numeric') for year in range(1940, 2041, 1)]
    hierarchy = Hierarchy('TM1py Year', 'TM1py Year', elements)
    dimension = Dimension('TM1py Year', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    elements = [Element('Q' + str(q), 'Numeric') for q in range(1, 5, 1)]
    hierarchy = Hierarchy('TM1py Quarter', 'TM1py Quarter', elements)
    dimension = Dimension('TM1py Quarter', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    elements = [Element('GDP', 'Numeric')]
    hierarchy = Hierarchy('TM1py Econ Measure', 'TM1py Econ Measure', elements)
    dimension = Dimension('TM1py Econ Measure', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    cube = Cube('TM1py Econ', ['TM1py Country', 'TM1py Year', 'TM1py Quarter', 'TM1py Econ Measure'])
    if not tm1.cubes.exists(cube.name):
        tm1.cubes.create(cube)

    # create stuff for stock sample
    instruments = ('IBM', 'AAPL', 'GOOG')
    elements = [Element(instrument, 'Numeric') for instrument in instruments]
    hierarchy = Hierarchy('TM1py Financial Instrument', 'TM1py Financial Instrument', elements)
    dimension = Dimension('TM1py Financial Instrument', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    measures = ('Open', 'High', 'Low', 'Close', 'Volume', 'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close',
                'Adj. Volume')
    elements = [Element(measure, 'Numeric') for measure in measures]
    hierarchy = Hierarchy('TM1py Stock Prices Measure', 'TM1py Stock Prices Measure', elements)
    dimension = Dimension('TM1py Stock Prices Measure', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    cube = Cube('TM1py Stock Prices', ['TM1py Financial Instrument', 'TM1py Date', 'TM1py Stock Prices Measure'])
    if not tm1.cubes.exists(cube.name):
        tm1.cubes.create(cube)
