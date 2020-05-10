"""
Create a new dimension TM1py Big dimension with 100,000 elements and some consolidations
"""
import configparser

from TM1py.Objects import Dimension, Hierarchy, Element
from TM1py.Services import TM1Service
from TM1py.Utils import Utils

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

DIMENSION_NAME = "TM1py Big Dimension"

# Establish connection to TM1 Server
with TM1Service(**config['tm1srv01']) as tm1:
    # Create Elements, Edges and stuff in python
    elements = [Element('Element {}'.format(i), 'Numeric') for i in range(1, 100001)]
    elements.append(Element('Even', 'Consolidated'))
    elements.append(Element('Odd', 'Consolidated'))
    elements.append(Element('4 Digit', 'Consolidated'))
    elements.append(Element('3 Digit', 'Consolidated'))

    edges = Utils.CaseAndSpaceInsensitiveTuplesDict()
    for i in range(2, 100001, 2):
        parent_child = ('Even', 'Element {}'.format(i))
        edges[parent_child] = 1

    for i in range(1, 100001, 2):
        parent_child = ('Odd', 'Element {}'.format(i))
        edges[parent_child] = 1

    for i in range(1000, 9999, 1):
        parent_child = ('4 Digit', 'Element {}'.format(i))
        edges[parent_child] = 1

    for i in range(100, 999, 1):
        parent_child = ('3 Digit', 'Element {}'.format(i))
        edges[parent_child] = 1

    hierarchy = Hierarchy(name=DIMENSION_NAME, dimension_name=DIMENSION_NAME, elements=elements, edges=edges)
    dimension = Dimension(name=DIMENSION_NAME, hierarchies=[hierarchy])

    # Send everything to TM1
    tm1.dimensions.create(dimension)
