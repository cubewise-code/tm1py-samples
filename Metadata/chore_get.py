"""
Get a chore from TM1
"""
import configparser

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

# Connection to TM1 Server
with TM1Service(**config['tm1srv01']) as tm1:
    # Read Chore:
    c = tm1.chores.get('Cub.GeneralLedger.Demo')

    # Print out the tasks
    for task in c.tasks:
        print("Process: {} Parameters: {}".format(task, task.parameters))
