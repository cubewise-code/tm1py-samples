"""
Run loose statements of TI
"""


from TM1py.Services import TM1Service

with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:
    ti_statements = [
        "DimensionCreate ( 'TM1py' );",
        "DimensionElementInsert ( 'TM1py' , '' , 'tm1' , 'N');",
        "DimensionElementInsert ( 'TM1py' , '' , 'is' , 'N');",
        "DimensionElementInsert ( 'TM1py' , '' , 'awesome' , 'N');"
    ]
    tm1.processes.execute_ti_code(lines_prolog=ti_statements, lines_epilog=[])

    ti_statements = [
        "SaveDataAll;",
        "DeleteAllPersistentFeeders;",
        "SecurityRefresh;",
        "CubeProcessFeeders('Plan_BudgetPlan');"
    ]
    tm1.processes.execute_ti_code(lines_prolog=ti_statements, lines_epilog=[])
