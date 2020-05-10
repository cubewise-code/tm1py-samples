"""
Read FX data from ECB (European Central Bank) through pandas and push it to the fx cube

Prerequisites:
Create the required cubes and dimensions:
->    Run TM1py sample "Load Data\ECB sample setup.py"
"""

import configparser
import xml.etree.ElementTree as ET

import requests
from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

# FX Cube Name
cube_name = 'ECB TM1py FX Rates'

# ECB XML interface https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml

# Get response from https request and parse XML into root
# Enable one of the two URLs below
url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml'
response = requests.get(url)
root = ET.fromstring(response.content)

# Container to store data that we write to TM1 in the end (in one batch)
cellset = dict()

date_prior = ''
for child in root.iter('{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube'):
    # Set time when the time tag is encountered
    if 'time' not in child.attrib:
        date = date_prior
    else:
        date = child.get('time')
    date_prior = date

    # Create dataset when we have a currency tag
    if 'currency' in child.attrib:
        coordinates = ('EUR', child.get('currency'), date, 'Spot')
        cellset[coordinates] = child.get('rate')

with TM1Service(**config['tm1srv01']) as tm1:
    tm1.cubes.cells.write_values(cube_name, cellset)
