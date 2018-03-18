from datetime import datetime

from TM1py.Services import TM1Service


with TM1Service(address='10.77.19.60', port=12354, user='admin', password='apple', ssl=True) as tm1:

    # Timestamp for Message-Log parsing
    timestamp = datetime(year=2018, month=2, day=15, hour=16, minute=2, second=0)

    # Get all entries since timestamp
    entries = tm1.server.get_transaction_log_entries(since=timestamp)

    # loop through entries
    for entry in entries:
        # Do stuff
        print(entry['TimeStamp'], entry)
