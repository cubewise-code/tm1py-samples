"""
Write Asynchronously to TM1 through the 'write_values_through_cellset' function.
Script creates cube and dimensions by default if they don't exist yet.

Play around with the number of working threads to find the optimal setup for your system!

"""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

from TM1py.Objects import Cube, Dimension, Element, Hierarchy
from TM1py.Services import TM1Service


# MDX Template
mdx_template = "SELECT " \
               "{{ SUBSET ([Big Dimension].Members, {}, {} ) }} on ROWS, " \
               "{{ [Python Cube Measure].[Numeric Element] }} on COLUMNS " \
               "FROM [Python Cube]"


# Create Dimensions and Cube, if it doesnt already exist
def create_dimensions_and_cube():
    with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:
        # Build Measure Dimension
        element = Element('Numeric Element', 'Numeric')
        hierarchy1 = Hierarchy('Python Cube Measure', 'Python Cube Measure', [element])
        dimension1 = Dimension('Python Cube Measure', [hierarchy1])
        if not tm1.dimensions.exists(dimension1.name):
            tm1.dimensions.create(dimension1)

        # Build Index Dimension
        elements = [Element(str(num), 'Numeric') for num in range(1, 100000)]
        hierarchy2 = Hierarchy('Big Dimension', 'Big Dimension', elements)
        dimension2 = Dimension('Big Dimension', [hierarchy2])
        if not tm1.dimensions.exists(dimension2.name):
            tm1.dimensions.create(dimension2)

        cube = Cube('Python Cube', [dimension2.name, dimension1.name])
        if cube.name not in tm1.cubes.get_all_names():
            tm1.cubes.create(cube)


# Function to be called in parallel
def write_values(tm1, mdx, values):
    print('start with mdx: {}'.format(mdx))
    tm1.data.write_values_through_cellset(mdx=mdx, values=values)
    print('Done with mdx: {}'.format(mdx))


# Now fire requests asynchronously
async def main():
    loop = asyncio.get_event_loop()
    with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [loop.run_in_executor(executor, write_values, tm1,
                                            mdx_template.format(0, 9999), range(0, 9999)),
                       loop.run_in_executor(executor, write_values, tm1,
                                            mdx_template.format(9999, 19999), range(9999, 19999)),
                       loop.run_in_executor(executor, write_values, tm1,
                                            mdx_template.format(19999, 39999), range(19999, 29999)),
                       loop.run_in_executor(executor, write_values, tm1,
                                            mdx_template.format(29999, 49999), range(29999, 39999)),
                       loop.run_in_executor(executor, write_values, tm1,
                                            mdx_template.format(39999, 59999), range(39999, 49999)),
                       loop.run_in_executor(executor, write_values, tm1,
                                            mdx_template.format(49999, 69999), range(49999, 59999)),
                       loop.run_in_executor(executor, write_values, tm1,
                                            mdx_template.format(59999, 79999), range(59999, 69999)),
                       loop.run_in_executor(executor, write_values, tm1,
                                            mdx_template.format(69999, 89999), range(69999, 79999)),
                       loop.run_in_executor(executor, write_values, tm1,
                                            mdx_template.format(79999, 99999), range(79999, 89999)),
                       loop.run_in_executor(executor, write_values, tm1,
                                            mdx_template.format(89999, 99999), range(89999, 99999))]
            for future in futures:
                await future

# Create everything if needed
create_dimensions_and_cube()

# Run it (and time it)
start_time_total = time.time()
print("Starting")
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
run_time = time.time() - start_time_total
print('Time: {:.4f} sec'.format(run_time))
