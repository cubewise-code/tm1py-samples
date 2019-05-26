"""
Create a TI process in TM1
"""
import configparser

from TM1py.Objects import Process
from TM1py.Services import TM1Service

config = configparser.ConfigParser()
config.read(r'..\config.ini')

# connection to TM1 Server
with TM1Service(**config['tm1srv01']) as tm1:
    process_name = 'TM1py process'

    # create new Process in python
    p_ascii = Process(name=process_name,
                      datasource_type='ASCII',
                      datasource_ascii_delimiter_char=',',
                      datasource_data_source_name_for_server=r'C:\Data\file.csv',
                      datasource_data_source_name_for_client=r'C:\Data\file.csv')
    # variables
    p_ascii.add_variable('v_1', 'Numeric')
    p_ascii.add_variable('v_2', 'Numeric')
    p_ascii.add_variable('v_3', 'Numeric')
    p_ascii.add_variable('v_4', 'Numeric')
    # parameters
    p_ascii.add_parameter(name='pCompanyCode', prompt='', value='DE04')
    # code
    p_ascii.prolog_procedure = "sText = 'IBM Cognos TM1';"
    # create process on TM1 Server
    tm1.processes.create(p_ascii)
