"""
Create a Chore.

Assumption: Process 'import actuals' exists in TM1 model and has a parameter 'pRegion'
"""
import configparser
import uuid
from datetime import datetime

from TM1py.Objects import Chore, ChoreStartTime
from TM1py.Objects import ChoreFrequency
from TM1py.Objects import ChoreTask
from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

# connection to TM1 Server
with TM1Service(**config['tm1srv01']) as tm1:
    now = datetime.now()
    frequency = ChoreFrequency(days='7', hours='9', minutes='2', seconds='45')
    tasks = [ChoreTask(0, 'import_actuals', parameters=[{'Name': 'pRegion', 'Value': 'UK'}])]
    # create an instance of TM1py.Objects.Chore in python
    c = Chore(name='TM1py_' + str(uuid.uuid4()),
              start_time=ChoreStartTime(now.year, now.month, now.day, now.hour, now.minute, now.second),
              dst_sensitivity=False,
              active=True,
              execution_mode='SingleCommit',
              frequency=frequency,
              tasks=tasks)
    # create the new chore in TM1
    tm1.chores.create(c)
