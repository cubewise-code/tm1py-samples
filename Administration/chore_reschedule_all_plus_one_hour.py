"""
Reschedule all chores by -1 Hour.
Chores get deactivated implicitly before update (and activate after transaction is done)

"""
import configparser

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

with TM1Service(**config['tm1srv01']) as tm1:
    # Get all chores. Loop through them and update them
    for chore in tm1.chores.get_all():
        chore.reschedule(hours=-1)
        tm1.chores.update(chore)
