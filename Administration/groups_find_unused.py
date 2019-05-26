"""
Find all security groups, that are not used
"""
import configparser

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
config.read(r'..\config.ini')

with TM1Service(**config['tm1srv01']) as tm1:
    # Get all groups
    all_groups = tm1.security.get_all_groups()

    # Determine the used groups from }ClientGroups Cube
    mdx = "SELECT " \
          "NON EMPTY {TM1SUBSETALL( [}Clients] )} on ROWS, " \
          "NON EMPTY {TM1SUBSETALL( [}Groups] )} ON COLUMNS " \
          "FROM [}ClientGroups]"
    cube_content = tm1.cubes.cells.execute_mdx(mdx, ['Value'])

    used_groups = {cell['Value'] for cell in cube_content.values() if cell['Value'] != ''}

    # Determine the unused groups
    unused_groups = set(all_groups) - used_groups

    # Print out the unused groups
    print(unused_groups)
