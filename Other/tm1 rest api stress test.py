"""
Do REST API operations in parallel. Can be handy when troubleshooting REST API bugs.
"""


import asyncio

from TM1py.Services import TM1Service

# define functions
def get_server_name(tm1):
    for i in range(1000):
        data = tm1.server.get_server_name()

def get_product_version(tm1):
    for i in range(1000):
        data = tm1.server.get_product_version()

def get_all_dimension_names(tm1):
    for i in range(1000):
        data = tm1.dimensions.get_all_names()

def get_all_process_names(tm1):
    for i in range(1000):
        data = tm1.processes.get_all_names()

def read_pnl(tm1):
    for i in range(1000):
        data = tm1.cubes.cells.get_view_content('Plan_BudgetPlan', 'High Level Profit and Loss', private=False)

# fire requests asynchronously
async def main():
    loop = asyncio.get_event_loop()
    with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:

        future1 = loop.run_in_executor(None, get_product_version, tm1)
        future2 = loop.run_in_executor(None, get_server_name, tm1)
        future3 = loop.run_in_executor(None, read_pnl, tm1)
        future4 = loop.run_in_executor(None, get_all_dimension_names, tm1)
        future5 = loop.run_in_executor(None, get_all_process_names, tm1)
        response1, response, response3, response4, response5 = \
            await future1, await future2, await future3, await future4, await future5

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
