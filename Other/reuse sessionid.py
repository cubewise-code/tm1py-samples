import time
from TM1py.Services import TM1Service

# Connect to TM1
tm1 = TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True)
print(tm1.server.get_server_name())
# Save TM1Service instance to file
tm1.save_to_file('tm1_connection')

time.sleep(7)

# Restore TM1Service instance from file
tm1 = TM1Service.restore_from_file('tm1_connection')
print(tm1.server.get_server_name())

# Logout
tm1.logout()