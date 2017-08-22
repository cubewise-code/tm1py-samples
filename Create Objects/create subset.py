"""
- Create new private Subset in TM1
- Read the subset and its elements
- Delete the subset in TM1
"""


from TM1py.Objects import Subset
from TM1py.Services import TM1Service


with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:
    subset_name = "Key Departments"

    # create subset
    s = Subset(dimension_name='Plan_Department', subset_name=subset_name, alias='', elements=['200', '405', '410'])
    tm1.subsets.create(subset=s, private=True)

    # get it and print out the elements
    s = tm1.subsets.get(dimension_name='Plan_Department', subset_name=subset_name, private=True)
    print(s.elements)

    # delete it
    tm1.subsets.delete(dimension_name='Plan_Department', subset_name=subset_name, private=True)

