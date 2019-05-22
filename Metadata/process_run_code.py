"""
Run loose statements of TI
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from TM1py.Services import TM1Service

with TM1Service(**config['tm1srv01']) as tm1:

    # Sample 1
    ti_statements = [
        "DimensionCreate ( 'TM1py' );",
        "DimensionElementInsert ( 'TM1py' , '' , 'tm1' , 'N');",
        "DimensionElementInsert ( 'TM1py' , '' , 'is' , 'N');",
        "DimensionElementInsert ( 'TM1py' , '' , 'awesome' , 'N');"
    ]
    tm1.processes.execute_ti_code(lines_prolog=ti_statements, lines_epilog=[])

    # Sample 2
    ti_statements = [
        "SaveDataAll;",
        "DeleteAllPersistentFeeders;",
        "SecurityRefresh;",
        "CubeProcessFeeders('Plan_BudgetPlan');"
    ]
    tm1.processes.execute_ti_code(lines_prolog=ti_statements, lines_epilog=[])
