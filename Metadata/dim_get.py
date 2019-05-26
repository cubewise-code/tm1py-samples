"""
Get a random dimension from the TM1 model and print out its details
"""
import configparser
import random

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
config.read(r'..\config.ini')

# Connection to TM1. Needs Address, Port, Credentials, and SSL
with TM1Service(**config['tm1srv01']) as tm1:
    # get random dimension from the model
    dimension_names = tm1.dimensions.get_all_names()
    random_number = random.randint(1, len(dimension_names))
    dimension = tm1.dimensions.get(dimension_name=dimension_names[random_number])

    # iterate through hierarchies
    for hierarchy in dimension:
        print('Hierarchy Name: {}'.format(hierarchy.name))
        # iterate through Elements in hierarchy
        for element in hierarchy:
            print('Element Name: {} Index: {} Type: {}'.format(element.name, str(element.index), element.element_type))
        # iterate through Subsets
        for subset in hierarchy.subsets:
            print('Subset Name: {}'.format(subset))
        # iterate through Edges
        for parent, child in hierarchy.edges:
            print("Parent Name: {}, Component Name: {}".format(parent, child))

        # print the default member
        print('Default Member: {}'.format(hierarchy.default_member))
