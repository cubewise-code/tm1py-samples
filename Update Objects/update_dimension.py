"""
Get a dimension. Update it and push it back to TM1.

IMPORTANT: Will not work TM1 11 due to bug in TM1
https://www.ibm.com/developerworks/community/forums/html/topic?id=75f2b99e-6961-4c71-9364-1d5e1e083eff&ps=25
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

import uuid

from TM1py.Services import TM1Service


# Connection to TM1. Needs Address, Port, Credentials, and SSL
with TM1Service(**config['tm1srv01']) as tm1:

    # get dimension
    dimension = tm1.dimensions.get('plan_department')

    # get the default hierarchy of the dimension
    h = dimension.hierarchies[0]

    # create new random element name
    parent = str(uuid.uuid4())
    child = str(uuid.uuid4())

    # add elements to hierarchy
    h.add_element(element_name=parent, element_type='Numeric')
    h.add_element(element_name=child, element_type='Numeric')

    # add edge to hierarchy
    h.add_edge(parent, child, 1000)

    # write Hierarchy back to TM1
    tm1.dimensions.update(dimension)
