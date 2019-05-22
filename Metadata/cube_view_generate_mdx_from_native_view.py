"""
Load existing cube view from TM1 into python. Then ask TM1py to generate the MDX Query from the cube view
"""

import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from TM1py.Services import TM1Service

cube = 'General Ledger'
view = 'P&L'

# Establish connection to TM1 Server
with TM1Service(**config['tm1srv01']) as tm1:

    # Instantiate TM1py.NativeView object
    nv = tm1.cubes.views.get_native_view(cube, view, private=False)

    # Retrieve MDX from native view. Print it
    print(nv.MDX)

