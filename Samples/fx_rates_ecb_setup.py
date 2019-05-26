"""
Create cubes and dimensions thar are required for the ECB Load Data Samples:
- ECB fx rates to cube

"""

import configparser
from datetime import timedelta, date

from TM1py.Objects import Cube, Dimension, Hierarchy, Element
from TM1py.Services import TM1Service

config = configparser.ConfigParser()
config.read(r'..\config.ini')


# Time magic with python generator
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


# push data to TM1
with TM1Service(**config['tm1srv01']) as tm1:
    # ============================
    # create TM1 objects for ECB fx rates sample
    currencies = (
        'EUR', 'USD', 'JPY', 'BGN', 'CZK', 'DKK', 'GBP', 'HUF', 'PLN', 'RON', 'SEK', 'CHF', 'ISK', 'NOK', 'HRK', 'RUB',
        'TRY', 'AUD', 'BRL', 'CAD', 'CNY', 'HKD', 'IDR', 'ILS', 'INR', 'LTL', 'LVL', 'EEK', 'KRW', 'MXN', 'MYR', 'NZD',
        'PHP', 'SGD', 'THB', 'ZAR', 'SKK', 'CYP', 'MTL', 'SIT', 'ROL', 'TRL')
    elements = [Element(cur, 'Numeric') for cur in currencies]

    # create dimension TM1py Currency From
    hierarchy = Hierarchy('TM1py Currency From', 'TM1py Currency From', elements)
    dimension = Dimension('TM1py Currency From', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create dimension TM1py Currency To
    hierarchy = Hierarchy('TM1py Currency To', 'TM1py Currency To', elements)
    dimension = Dimension('TM1py Currency To', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create dimension TM1py Date
    start_date = date(1990, 1, 1)
    end_date = date(2041, 1, 1)
    elements = [Element(str(single_date), 'Numeric') for single_date in daterange(start_date, end_date)]
    hierarchy = Hierarchy('TM1py Date', 'TM1py Date', elements)
    dimension = Dimension('TM1py Date', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create dimension TM1py Month
    elements = [Element(str(month), 'Numeric') for month in range(1, 13)]
    hierarchy = Hierarchy('TM1py Month', 'TM1py Month', elements)
    dimension = Dimension('TM1py Month', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create dimension TM1py Year
    elements = [Element(str(year), 'Numeric') for year in range(1990, 2041, 1)]
    hierarchy = Hierarchy('TM1py Year', 'TM1py Year', elements)
    dimension = Dimension('TM1py Year', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create dimension TM1py FX Rates Measure
    elements = [Element('Spot', 'Numeric'), Element('EOP', 'Numeric'),
                Element('AVG', 'Numeric'), Element('Month Close', 'Numeric')]
    hierarchy = Hierarchy('TM1py FX Rates Measure', 'TM1py FX Rates Measure', elements)
    dimension = Dimension('TM1py FX Rates Measure', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create cube TM1py FX Rates
    cube = Cube('ECB TM1py FX Rates',
                ['TM1py Currency From', 'TM1py Currency To', 'TM1py Date', 'TM1py FX Rates Measure'])
    if not tm1.cubes.exists(cube.name):
        tm1.cubes.create(cube)
