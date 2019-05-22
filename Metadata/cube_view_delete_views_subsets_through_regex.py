"""
Remove all Views and Subsets in TM1 that match a list of regular expressions.
use with care!
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

import re

from TM1py.Services import TM1Service

with TM1Service(**config['tm1srv01']) as tm1:
    # regular expression for everything that starts with 'temp_' or 'test_'
    regex_list = ['^temp_.*', '^test_.*']

    # iterate through cubes
    cubes = tm1.cubes.get_all_names()
    for cube in cubes:
        private_views, public_views = tm1.cubes.views.get_all(cube_name=cube)
        for view in private_views:
            for regex in regex_list:
                if re.match(regex, view.name, re.IGNORECASE):
                    tm1.cubes.views.delete(cube_name=cube, view_name=view.name, private=True)
        for view in public_views:
            for regex in regex_list:
                if re.match(regex, view.name, re.IGNORECASE):
                    tm1.cubes.views.delete(cube_name=cube, view_name=view.name, private=False)

    # iterate through dimensions
    dimensions = tm1.dimensions.get_all_names()
    for dimension in dimensions:
        subsets = tm1.dimensions.subsets.get_all_names(dimension_name=dimension, hierarchy_name=dimension)
        for subset in subsets:
            for regex in regex_list:
                if re.match(regex, subset, re.IGNORECASE):
                    tm1.dimensions.subsets.delete(dimension_name=dimension, subset_name=subset)
