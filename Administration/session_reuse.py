"""
Reuse session id to avoid (unreasonably slow) CAM Authentication
"""

from TM1py.Services import TM1Service
import configparser


config = configparser.ConfigParser()
config.read('..\config.ini')


# instantiate session
tm1_a = TM1Service(**config['tm1srv01'], logging=True)

# get session_id from tm1 connection
session_id = tm1_a.connection.session_id

# create a new TM1 connection (tm1_b) with same session as tm1_a
tm1_b = TM1Service(**config['tm1srv01'], session_id=session_id, logging=True)

# Do something...
print(tm1_b.server.get_server_name())

# End session
tm1_b.logout()
