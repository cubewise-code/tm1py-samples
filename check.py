"""
This script can be used to check if TM1py can connect to your TM1 instance
"""

import getpass
from distutils.util import strtobool

from TM1py.Services import TM1Service

# Parameters for connection
user = input("TM1 User (leave empty if SSO): ")
password = getpass.getpass("Password (cmd doesn't show input, leave empty if SSO): ")
namespace = input("CAM Namespace (leave empty if no CAM Security): ")
address = input("Address (leave empty if localhost): ")
gateway = input("ClientCAMURI (leave empty if no SSO): ")
port = input("HTTP Port: ")
ssl = strtobool(input("SSL (True or False): "))

if len(namespace.strip()) == 0:
    namespace = None

if len(gateway.strip()) == 0:
    gateway = None

with TM1Service(
        address=address,
        port=port,
        user=user,
        password=password,
        namespace=namespace,
        gateway=gateway,
        ssl=ssl) as tm1:
    server_name = tm1.server.get_server_name()
    print("Connection to TM1 established!! your Servername is: {}".format(server_name))
