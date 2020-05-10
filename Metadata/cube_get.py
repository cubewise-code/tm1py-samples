"""
Get a Cube from TM1
"""
import configparser

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

with TM1Service(**config['tm1srv01']) as tm1:
    c = tm1.cubes.get('General Ledger')
    print(c.name)
    print(c.dimensions)
    if c.has_rules:
        print(c.rules)
