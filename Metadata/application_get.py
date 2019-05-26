"""
Create a new file out.xlsx from a TM1 application file.
"""
import configparser

from TM1py import TM1Service

config = configparser.ConfigParser()
config.read(r'..\config.ini')

with TM1Service(**config['tm1srv01']) as tm1:
    # path in TM1 Application-Tree
    path = 'Finance/P&L.xlsx'

    # get the application
    application = tm1.applications.get(path)

    # write it to xlsx file
    application.to_xlsx("out.xlsx")
