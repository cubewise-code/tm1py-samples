"""
Query all cubes from TM1. 
For each cube calculate the number of potential cells.
"""

import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

import json

from TM1py.Services import TM1Service


with TM1Service(**config['tm1srv01']) as tm1:
    # New List to store the cube - number mapping
    cubes_with_cellnumber = []
    # Loop through cubes and do the math
    for cube in tm1.cubes.get_all():
        cube.numberCells = 1
        for dimension_name in cube.dimensions:
            response = tm1._tm1_rest.GET('/api/v1/Dimensions(\'{}\')/Hierarchies(\'{}\')/Elements/$count'
                                         .format(dimension_name, dimension_name))
            number = int(response.text)
            cube.numberCells *= number
        cubes_with_cellnumber.append(cube)
    # Sort the cube list with a lambda expr.
    cubes_with_cellnumber.sort(key=lambda c: c.numberCells, reverse=True)
    # Print the results
    for cube in cubes_with_cellnumber:
        print('Cube: {}, Cells: {}'.format(cube.name, cube.numberCells))
