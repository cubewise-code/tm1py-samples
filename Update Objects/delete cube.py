""" 
Delete a cube
"""

from TM1py.Services import TM1Service

with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:
    tm1.cubes.delete('Rubiks Cube')
