"""
Get a dimension. Update it and push it back to TM1.
"""

import uuid

from TM1py.Services import TM1Service


# Connection to TM1. Needs Address, Port, Credentials, and SSL
with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:

    # get dimension
    dimension = tm1.dimensions.get('plan_department')

    # get the default hierarchy of the dimension
    h = dimension.hierarchies[0]

    # create new random element name
    element_name = str(uuid.uuid4())

    # add element to hierarchy
    h.add_element(element_name=element_name, element_type='Numeric')

    # add edge to hierarchy
    h.add_edge('TM1py elem', element_name, 1000)

    # write Hierarchy back to TM1
    tm1.dimensions.update(dimension)
