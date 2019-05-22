""" 
Get Chore form TM1. Update it. Push it back to TM1.
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from TM1py.Objects import ChoreFrequency
from TM1py.Services import TM1Service

# Connection to TM1 Server
with TM1Service(**config['tm1srv01']) as tm1:

    # Read chore:
    c = tm1.chores.get('real chore')

    # Update properties
    c.reschedule(minutes=-3)
    c._frequency = ChoreFrequency(days=7, hours=22, minutes=5, seconds=1)
    c._execution_mode = 'MultipleCommit'
    c.activate()

    # Update the TM1 chore
    tm1.chores.update(c)


