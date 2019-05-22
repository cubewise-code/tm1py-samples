"""
Remove all objects in TM1 that match a list of regular expressions.
use with care!
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

import re

from TM1py.Services import TM1Service


with TM1Service(**config['tm1srv01']) as tm1:

    # Regular expression for everything that starts with 'temp_', 'test' or 'TM1py'
    regex_list = ['^temp_*', '^test*', '^TM1py*']

    # Iterate through cubes
    cube_names = tm1.cubes.get_all_names()
    for cube_name in cube_names:
        for regex in regex_list:
            if re.match(regex, cube_name, re.IGNORECASE):
                tm1.cubes.delete(cube_name)
                break
            else:
                private_view_names, public_views_names = tm1.cubes.views.get_all_names(cube_name=cube_name)
                for view_name in private_view_names:
                    if re.match(regex, view_name, re.IGNORECASE):
                        tm1.cubes.views.delete(cube_name=cube_name, view_name=view_name, private=True)
                for view_name in private_view_names:
                    if re.match(regex, view_name, re.IGNORECASE):
                        tm1.cubes.views.delete(cube_name=cube_name, view_name=view_name, private=False)

    # Get Dimension names. Filter out Control Dimensions
    dimension_names = [dimension for dimension in tm1.dimensions.get_all_names() if not dimension.startswith('}')]
    # Iterate through dimensions
    for dimension_name in dimension_names:
        for regex in regex_list:
            if re.match(regex, dimension_name, re.IGNORECASE):
                tm1.dimensions.delete(dimension_name)
                break
            else:
                # Iterate through public subsets
                subsets = tm1.dimensions.subsets.get_all_names(dimension_name=dimension_name,
                                                               hierarchy_name=dimension_name,
                                                               private=False)
                for subset in subsets:
                    if re.match(regex, subset, re.IGNORECASE):
                        tm1.dimensions.subsets.delete(dimension_name=dimension_name, subset_name=subset, private=False)

    # Iterate through Chores
    chores = tm1.chores.get_all_names()
    for chore in chores:
        for regex in regex_list:
            if re.match(regex, chore, re.IGNORECASE):
                tm1.chores.delete(chore)

    # Iterate through Processes
    processes = tm1.processes.get_all_names()
    for process in processes:
        for regex in regex_list:
            if re.match(regex, process, re.IGNORECASE):
                tm1.processes.delete(process)

