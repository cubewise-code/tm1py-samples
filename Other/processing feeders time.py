"""
regenerate feeders for all cubes. Read the time it took from the MessageLog and print it out
"""

import time as t
from datetime import date, time, datetime

from TM1py.Services import TM1Service


# Time magic with python
def get_time_from_tm1_timestamp(tm1_timestamp):
    f = lambda x: int(x) if x else 0
    year = f(tm1_timestamp[0:4])
    month = f(tm1_timestamp[5:7])
    day = f(tm1_timestamp[8:10])
    hour = f(tm1_timestamp[11:13])
    minute = f(tm1_timestamp[14:16])
    second = f(tm1_timestamp[17:19])
    return datetime.combine(date(year, month, day), time(hour, minute, second))

# Connect to TM1
with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:
    for cube in tm1.cubes.get_all():
        if cube.has_rules and cube.rules.has_feeders:
            ti = 'CubeProcessFeeders(\'{}\');'.format(cube.name)
            # Process feeders for cube
            tm1.processes.execute_ti_code(lines_prolog=[ti], lines_epilog='')

            # Give TM1 a second so that it can write an entry into the messagelog
            t.sleep(1)

            # Get logs
            logs = tm1.server.get_message_log_entries(reverse=True, top=100)

            # Filter logs
            filtered_logs = (entry for entry
                             in logs
                             if entry['Logger'] == 'TM1.Server' and 'TM1CubeImpl::ProcessFeeders' in entry['Message']
                             and cube.name in entry['Message'])

            # Get start time and end time
            endtime_processing = next(filtered_logs)['TimeStamp']
            starttime_processing = next(filtered_logs)['TimeStamp']

            # Calculate Delta
            start = get_time_from_tm1_timestamp(starttime_processing)
            end = get_time_from_tm1_timestamp(endtime_processing)
            delta = end-start
            print("Cube: {} | Time for processing Feeders: {}".format(cube.name, delta))
