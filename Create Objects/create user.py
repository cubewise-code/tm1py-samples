"""
Create a new user
"""

from TM1py.Objects import User
from TM1py.Services import TM1Service


with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:
    u = User(name='Hodor Hodor', friendly_name='Hodor', groups=['Admin'], password='apple')
    tm1.security.create(u)
