"""
Create a new user
"""
import configparser

from TM1py.Objects import User
from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

with TM1Service(**config['tm1srv01']) as tm1:
    u = User(name='Hodor Hodor', friendly_name='Hodor', groups=['Admin'], password='apple')
    tm1.security.create_user(u)
