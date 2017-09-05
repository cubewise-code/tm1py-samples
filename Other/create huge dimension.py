from TM1py.Services import TM1Service
from TM1py.Objects import Dimension, Hierarchy, Element
from TM1py.Utils import Utils

# Establish connection to TM1 Server
with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:
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

    hierarchy = Hierarchy('TM1py Big Dimension', 'TM1py Big Dimension', elements, edges=edges)
    dimension = Dimension('TM1py Big Dimension', [hierarchy])

    # Send everything to TM1
    tm1.dimensions.create(dimension)
