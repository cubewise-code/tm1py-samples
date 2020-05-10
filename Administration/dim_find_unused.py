"""
Find all dimensions, that are not used in cubes
"""
import configparser

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

# Connect to TM1
with TM1Service(**config['tm1srv01']) as tm1:
    # get all dimensions
    all_dimensions = tm1.dimensions.get_all_names()
    # get all cubes
    all_cubes = tm1.cubes.get_all()
    # find used dimensions
    used_dimensions = set()
    for cube in all_cubes:
        used_dimensions.update(cube.dimensions)
    # determine unused dimensions
    unused_dimensions = set(all_dimensions) - used_dimensions

    print(unused_dimensions)
