"""
Create a cube with 4 dimensions: red, green, blue, yellow

Assumption: Dimensions (red, green, blue, yellow) exist in tm1 model
"""
import configparser

from TM1py.Objects import Cube
from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

# connection to TM1 Server
with TM1Service(**config['tm1srv01']) as tm1:
    cube = Cube(name='Rubiks Cube', dimensions=['red', 'green', 'blue', 'yellow'], rules='')
    tm1.cubes.create(cube)
