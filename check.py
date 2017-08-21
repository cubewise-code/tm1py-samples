"""
This script can be used to check if TM1py can connect to your TM1 instance
"""

import getpass
from distutils.util import strtobool
from TM1py.Services import TM1Service

# Parameters for connection
user = input("TM1 User: ")
password = getpass.getpass("Password: ")
address = input("Address: ")
port = input("Port: ")
ssl = strtobool(input("SSL (True or False): "))

with TM1Service(address=address, port=port, user=user, password=password, ssl=ssl) as tm1:
    server_name = tm1.server.get_server_name()
    print("Connection to TM1 established!! your Servername is: {}".format(server_name))
