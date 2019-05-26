"""
When a dimension of a cube is not explicitly referenced in an MDX Query,
TM1 will implicitly use the DefaultMember for the missing dimension.
If no DefaultMember is defined in TM1, it will use the element with index 1.

You can use TM1py to query and update the default member for a Hierarchy
"""

import configparser

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
config.read(r'..\config.ini')

with TM1Service(**config['tm1srv02']) as tm1:
    new_default_member = "2019-01-01"
    tm1.dimensions.hierarchies.update_default_member(
        dimension_name="Date",
        hierarchy_name="Date",
        member_name=new_default_member)
