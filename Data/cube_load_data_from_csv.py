"""
Read a csv file with ~ 1000000 lines and write the data to a cube
Takes about 24 seconds.
"""
import configparser
import time

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

# Build cellset from file
cube = ''
cellset = {}

# Line 1: "Planning Sample:plan_BudgetPlan";"FY 2003 Budget";"10110";"105";"41101";"local";"input";"Jan-2003";315512.69
with open("plan_BudgetPlan.csv", "r") as file:
    # Read coordinates and values from each line
    for line in file:
        entries = line.split(";")
        coordinates = tuple([coordinate[1:-1] for coordinate in entries[1:-1]])
        value = entries[-1]
        cellset[coordinates] = value
    # Read cube name from the last line in the file
    server_and_cube = line.split(";")[0]
    cube = server_and_cube.split(":")[1][0:-1]

# Push cellset to TM1
with TM1Service(**config['tm1srv01']) as tm1:
    start = time.time()
    tm1.cubes.cells.write_values(cube, cellset)
    end = time.time()
    print("Cells per Second: {}".format(len(cellset) / (end - start)))
