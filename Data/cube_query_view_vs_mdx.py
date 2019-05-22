"""
Query data through MDX and cube view. 
Measure time to see which way is faster.

Assumption: Cube 'Plan_BudgetPlan' has a view called 'PerformanceTest'
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

import time

from TM1py.Services import TM1Service

with TM1Service(**config['tm1srv01']) as tm1:

    cube_name = 'General Ledger'
    view_name = 'Default'

    # Extract MDX from CubeView
    mdx = tm1.cubes.views.get_native_view(cube_name, view_name, private=False).MDX
    print(mdx)

    # Results List
    runtimes_view = []
    runtimes_mdx = []

    # Query data through CubeView
    for i in range(20):
        start_time = time.time()
        a = tm1.cubes.cells.execute_view(cube_name, view_name, private=False)
        run_time = time.time() - start_time
        runtimes_view.append(run_time)

    # Query data through MDX
    for j in range(20):
        start_time = time.time()
        b = tm1.cubes.cells.execute_mdx(mdx)
        run_time = time.time() - start_time
        runtimes_mdx.append(run_time)

    print("View: " + str(sum(runtimes_view)/len(runtimes_view)))
    print("MDX: " + str(sum(runtimes_mdx) / len(runtimes_mdx)))

    print('Data is the same, right? {}'.format(a == b))


