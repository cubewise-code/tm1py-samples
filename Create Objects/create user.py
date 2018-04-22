"""
Create a new user
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from TM1py.Objects import User
from TM1py.Services import TM1Service


with TM1Service(**config['tm1srv01']) as tm1:
    u = User(name='Hodor Hodor', friendly_name='Hodor', groups=['Admin'], password='apple')
    tm1.security.create_user(u)
