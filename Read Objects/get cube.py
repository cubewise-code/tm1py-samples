"""
Get a Cube from TM1
"""

from TM1py.Services import TM1Service


with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:
    c = tm1.cubes.get('Rubiks Cube')
    print(c.name)
    print(c.dimensions)
    if c.has_rules:
        print(c.rules)
