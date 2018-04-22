""" 
Delete a cube
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from TM1py.Services import TM1Service

with TM1Service(**config['tm1srv01']) as tm1:
    tm1.cubes.delete('Rubiks Cube')
