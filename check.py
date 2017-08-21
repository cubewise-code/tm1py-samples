"""
This script can be used to check if TM1py can connect to your TM1 instance
"""

from TM1py.Services import TM1Service

# Parameters for connection
user = 'admin'
password = 'apple'
address = ''
port = 8001
ssl = False

with TM1Service(address=address, port=port, user='admin', password='apple', ssl=ssl) as tm1:
    server_name = tm1.server.get_server_name()
    print("Connection to TM1 established!! your Servername is: {}".format(server_name))
