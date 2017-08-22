""" 
Get a Process from TM1. Update it. Push it back to TM1.
"""

from TM1py.Services import TM1Service

# connection to TM1 Server
with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:
    # read process
    p = tm1.processes.get('TM1py process')

    # modify process
    p.datasource_type = 'None'
    p.epilog_procedure = "nRevenue = 100000;\r\nsCostCenter = 'UK01';"
    p.remove_parameter('pCompanyCode')
    p.add_parameter('pBU', prompt='', value='UK02')

    # update
    tm1.processes.update(p)

