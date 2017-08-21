"""
Remove all objects in TM1 that match a list of regular expressions.

user with care! Very powerful!
"""



import re

from TM1py.Services import TM1Service


with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:

    # Regular expression for everything that starts with 'temp_', 'test' or 'TM1py'
    regex_list = ['^temp_*', '^test*', '^TM1py*']

    # Iterate through cubes
    cubes = tm1.cubes.get_all_names()
    for cube in cubes:
        for regex in regex_list:
            if re.match(regex, cube, re.IGNORECASE):
                tm1.cubes.delete(cube)
                break
            else:
                private_views, public_views = tm1.views.get_all(cube_name=cube)
                for view in private_views:
                    if re.match(regex, view.name, re.IGNORECASE):
                        tm1.views.delete(cube_name=cube, view_name=view.name, private=True)
                for view in public_views:
                    if re.match(regex, view.name, re.IGNORECASE):
                        tm1.views.delete(cube_name=cube, view_name=view.name, private=False)

    # Iterate through dimensions
    dimensions = tm1.dimensions.get_all_names()
    for dimension in dimensions:
        for regex in regex_list:
            if re.match(regex, dimension, re.IGNORECASE):
                tm1.dimensions.delete(dimension)
                # TM1 deletes the Element Attributes dimension independently, so we remove it from our list
                element_attributes_dimension = '}}ElementAttributes_{}'.format(dimension)
                if element_attributes_dimension in dimensions:
                    dimensions.remove(element_attributes_dimension)
                break
            else:
                subsets = tm1.subsets.get_all_names(dimension_name=dimension, hierarchy_name=dimension)
                for subset in subsets:
                    if re.match(regex, subset, re.IGNORECASE):
                        tm1.subsets.delete(dimension, subset)

    # Iterate through Processes
    processes = tm1.processes.get_all_names()
    for process in processes:
        for regex in regex_list:
            if re.match(regex, process, re.IGNORECASE):
                tm1.processes.delete(process)

