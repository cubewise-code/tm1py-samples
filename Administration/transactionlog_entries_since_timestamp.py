"""
Get all TM1 transactions for all cubes starting to a specific date.
"""

import configparser
from datetime import datetime

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

with TM1Service(**config['tm1srv01']) as tm1:
    # Timestamp for Message-Log parsing
    timestamp = datetime(year=2018, month=2, day=15, hour=16, minute=2, second=0)

    # Get all entries since timestamp
    entries = tm1.server.get_transaction_log_entries(since=timestamp)

    # loop through entries
    for entry in entries:
        # Do stuff
        print(entry['TimeStamp'], entry)
