"""
Load existing cube view from TM1 into python. Then ask TM1py to generate the MDX Query from the cube view
"""

from TM1py.Services import TM1Service


# Establish connection to TM1 Server
with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:

    # Instantiate TM1py.NativeView object
    nv = tm1.views.get_native_view('Plan_BudgetPlan', 'High Level Profit And Loss', private=False)

    # Retrieve MDX from native view. Print it
    print(nv.MDX)
