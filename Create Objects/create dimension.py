"""
Create a dimension with Elements, Edges and ElementAttributes

IMPORTANT: Will not work TM1 11 due to bug in TM1
https://www.ibm.com/developerworks/community/forums/html/topic?id=75f2b99e-6961-4c71-9364-1d5e1e083eff&ps=25
"""

from TM1py.Objects import Dimension, Element, ElementAttribute, Hierarchy
from TM1py.Services import TM1Service


name = 'TM1py Region'

# Connection to TM1. Needs IP, Port, Credentials, and SSL
with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:
    # create elements objects
    elements = [Element(name='Europe', element_type='Consolidated'),
                Element(name='CH', element_type='Numeric'),
                Element(name='UK', element_type='Numeric'),
                Element(name='BE', element_type='Numeric')]

    # create edge object
    edges = {('Europe', 'CH'): 1,
             ('Europe', 'UK'): 1,
             ('Europe', 'BE'): 1}

    # create the element_attributes
    element_attributes = [ElementAttribute(name='Name Long', attribute_type='Alias'),
                          ElementAttribute(name='Name Short', attribute_type='Alias'),
                          ElementAttribute(name='Currency', attribute_type='String')]

    # create hierarchy object
    hierarchy = Hierarchy(name=name, dimension_name=name, elements=elements, element_attributes=element_attributes,
                          edges=edges)

    # create dimension object
    d = Dimension(name=name, hierarchies=[hierarchy])

    # create dimension in TM1 !
    tm1.dimensions.create(d)


