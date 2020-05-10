"""
Do REST API operations in parallel. Can be handy when troubleshooting REST API bugs.
"""
import asyncio
import configparser

from TM1py.Services import TM1Service

CUBE_NAME = "General Ledger"
VIEW_NAME = "Default"

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')


# define functions
def get_server_name(tm1):
    for i in range(1000):
        data = tm1.server.get_server_name()


def execute_mdx(tm1):
    mdx = "SELECT { [}Clients].Members } ON ROWS, { [}Groups].Members } ON COLUMNS FROM [}ClientGroups]"
    for i in range(1000):
        data = tm1.cubes.cells.execute_mdx(mdx)


def get_all_dimension_names(tm1):
    for i in range(1000):
        data = tm1.dimensions.get_all_names()


def get_all_process_names(tm1):
    for i in range(1000):
        data = tm1.processes.get_all_names()


def read_pnl(tm1):
    for i in range(1000):
        data = tm1.cubes.cells.execute_view(CUBE_NAME, VIEW_NAME, private=False)


# fire requests asynchronously
async def main():
    loop = asyncio.get_event_loop()
    with TM1Service(**config['tm1srv01']) as tm1:
        future1 = loop.run_in_executor(None, execute_mdx, tm1)
        future2 = loop.run_in_executor(None, get_server_name, tm1)
        future3 = loop.run_in_executor(None, read_pnl, tm1)
        future4 = loop.run_in_executor(None, get_all_dimension_names, tm1)
        future5 = loop.run_in_executor(None, get_all_process_names, tm1)
        response1, response, response3, response4, response5 = \
            await future1, await future2, await future3, await future4, await future5


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
