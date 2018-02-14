"""
Read a csv file with ~ 1000000 lines and write the data to a cube
Takes about 24 seconds.

"""
import time

from TM1py.Services import TM1Service

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
with TM1Service(address="localhost", port=12354, user="admin", password="apple", ssl=True) as tm1:
    start = time.time()
    tm1.cubes.cells.write_values(cube, cellset)
    end = time.time()
    print("Cells per Second: {}".format(len(cellset)/(end-start)))
