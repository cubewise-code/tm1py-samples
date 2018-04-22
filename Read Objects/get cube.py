"""
Get a Cube from TM1
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from TM1py.Services import TM1Service

with TM1Service(**config['tm1srv01']) as tm1:
    c = tm1.cubes.get('General Ledger')
    print(c.name)
    print(c.dimensions)
    if c.has_rules:
        print(c.rules)
