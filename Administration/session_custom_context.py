"""
Instantiate TM1py with a custom session_context.
Session_context is displayed in column "session" in Arc
"""

import configparser

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
config.read('..\config.ini')

APP_NAME = "My TM1py Application"

with TM1Service(**config['tm1srv01'], session_context=APP_NAME) as tm1:
    dimensions = tm1.dimensions.get_all_names()
    for dim in dimensions:
        print(dim)
