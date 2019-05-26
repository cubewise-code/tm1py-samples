""" 
Delete a cube
"""
import configparser

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
config.read(r'..\config.ini')

with TM1Service(**config['tm1srv01']) as tm1:
    tm1.cubes.delete('Rubiks Cube')
