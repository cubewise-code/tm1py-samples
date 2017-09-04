"""
Query a Process from the TM1 model
"""

from TM1py.Services import TM1Service

# connection to TM1 Server
with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:
    # read Process
    p = tm1.processes.get('TM1py process')

    # print variables, parameters, ...
    print('Parameters: \r\n' + str(p.parameters))
    print('Variables: \r\n' + str(p.variables))
    print('Prolog: \r\n' + str(p.prolog_procedure))
    print('Metadata: \r\n' + str(p.metadata_procedure))
    print('Data: \r\n' + str(p.data_procedure))
    print('Epilog: \r\n' + str(p.epilog_procedure))

