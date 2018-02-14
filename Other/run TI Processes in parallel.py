""" 
Run Processes in parallel.
Requires Python 3.5 or greater
"""

import asyncio

from TM1py.Services import TM1Service

regions = ['DE', 'UK', 'US', 'BE', 'AU', 'JP', 'CN', 'NZ', 'FR', 'PL']
process = 'import_actuals'


# Define Function
def run_process(tm1, region):
    print("run process with parameter pRegion: " + region)
    parameters = {
        'Parameters': [{
            'Name': "pRegion",
            'Value': region
        }]
    }
    tm1.processes.execute(process, parameters)
    print("Done running Process for Region : " + region)

# Fire requests asynchronously
async def main():
    loop = asyncio.get_event_loop()
    # Connect to TM1
    with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:
        # Fire of different process executions though 'run_process' function.
        futures = [loop.run_in_executor(None, run_process, tm1, 'pRegion ' + regions[num])
                   for num
                   in range(1, 10)]
        # Await the executions
        for future in futures:
            await future


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
