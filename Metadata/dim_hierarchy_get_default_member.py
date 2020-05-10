"""
When a dimension of a cube is not explicitly referenced in an MDX Query,
TM1 will implicitly use the DefaultMember for the missing dimension.
If no DefaultMember is defined in TM1, it will use the element with index 1.

You can use TM1py to query and update the default member for a Hierarchy
"""

import configparser

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

with TM1Service(**config['tm1srv02']) as tm1:
    current_default_member = tm1.dimensions.hierarchies.get_default_member(
        dimension_name="Date",
        hierarchy_name="Date")
    print("Current default member for dimension Date: " + current_default_member)
