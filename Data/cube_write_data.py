"""
Write data to TM1
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from TM1py.Services import TM1Service

with TM1Service(**config['tm1srv01']) as tm1:
    # cellset to store the new data
    cellset = {}
    # Populate cellset with coordinates and value pairs
    cellset[('FY 2004 Budget', 'UK', 'Finance', 'Utilities', 'local', 'input', 'Apr-2005')] = 2312
    cellset[('FY 2004 Budget', 'UK', 'Finance', 'Utilities', 'local', 'input', 'May-2005')] = 2214
    cellset[('FY 2004 Budget', 'UK', 'Finance', 'Utilities', 'local', 'input', 'Jun-2005')] = 2451
    cellset[('FY 2004 Budget', 'UK', 'Finance', 'Utilities', 'local', 'input', 'Jul-2005')] = 2141
    cellset[('FY 2004 Budget', 'UK', 'Finance', 'Utilities', 'local', 'input', 'Aug-2005')] = 2621
    # send the cellset to TM1
    tm1.cubes.cells.write_values('Plan_BudgetPlan', cellset)
