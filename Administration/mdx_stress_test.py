"""
Do MDX Queries asynchronously. 
"""
import asyncio
import configparser

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

mdx1 = """
SELECT
NON EMPTY {[Date].[2017-01-01]:[Date].[2017-12-31]} * {[Bike Shares Measure].[Count]} ON ROWS,
NON EMPTY {[City].[NYC], [City].[Chicago]} ON COLUMNS
FROM [Bike Shares]
WHERE ([Version].[Actual])
"""

mdx2 = """
SELECT
NON EMPTY {[Date].[2016-01-01]:[Date].[2016-12-31]} * {[Bike Shares Measure].[Count]} ON ROWS,
NON EMPTY {[City].[NYC], [City].[Chicago]} ON COLUMNS
FROM [Bike Shares]
WHERE ([Version].[Actual])
"""

mdx3 = """
SELECT
NON EMPTY {[Date].[2015-01-01]:[Date].[2015-12-31]} * {[Bike Shares Measure].[Count]} ON ROWS,
NON EMPTY {[City].[NYC], [City].[Chicago]} ON COLUMNS
FROM [Bike Shares]
WHERE ([Version].[Actual])
"""


# Define function
def execute_mdx(tm1, mdx):
    data = tm1.cubes.cells.execute_mdx(mdx)
    print(len(data))
    # no Exceptions means success
    return True


# Fire requests asynchronously
async def main():
    loop = asyncio.get_event_loop()
    with TM1Service(**config['tm1srv01']) as tm1:
        outcomes = list()
        futures = list()
        for _ in range(50):
            futures.append(loop.run_in_executor(None, execute_mdx, tm1, mdx1))
            futures.append(loop.run_in_executor(None, execute_mdx, tm1, mdx2))
            futures.append(loop.run_in_executor(None, execute_mdx, tm1, mdx3))
        for future in futures:
            outcomes.append(await future)
        assert all(outcomes)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
