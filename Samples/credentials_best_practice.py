import configparser
from getpass import getpass

import keyring
from TM1py import TM1Service

INSTANCE = "tm1srv01"

config = configparser.ConfigParser()
config.read(r'..\config.ini')

address = config[INSTANCE]["address"]
port = config[INSTANCE]["port"]
ssl = config[INSTANCE]["ssl"]
user = config[INSTANCE]["user"]

# interact with Windows Credential Manager through the keyring library
password = keyring.get_password(INSTANCE, user)
if not password:
    password = getpass(f"Please insert password for user '{user}' and instance '{INSTANCE}':")
keyring.set_password(INSTANCE, user, password)

config[INSTANCE]["password"] = password

with TM1Service(**config[INSTANCE]) as tm1:
    tm1_version = tm1.server.get_product_version()
    print(tm1_version)
