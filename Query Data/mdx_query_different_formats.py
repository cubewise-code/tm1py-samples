"""
Query a default TM1 "Planning Sample" server and show results in different formats
"""

import pprint
import configparser

from TM1py.Services import TM1Service
from TM1py.Utils import Utils

# Read Config
config = configparser.ConfigParser()
config.read('..\config.ini')

# Initializer Prettyprinter
pp = pprint.PrettyPrinter(indent=2)

# Connect to TM1
with TM1Service(**config['tm1srv01']) as tm1:

    mdx = """
        SELECT
        NON EMPTY {[plan_time].[Q1-2004],[plan_time].[Q2-2004],[plan_time].[Q3-2004],[plan_time].[Q4-2004]} on COLUMNS,
        NON EMPTY {[plan_chart_of_accounts].[Revenue],[plan_chart_of_accounts].[Net Operating Income]} on ROWS
        FROM [plan_Report]
        WHERE (
            [plan_business_unit].[Total Business Unit], 
            [plan_department].[Total Organization],
            [plan_exchange_rates].[actual],
            [plan_report].[Budget]
            )
        """

    # raw: native response dictionary
    raw_data = tm1.cubes.cells.execute_mdx_raw(
        mdx=mdx,
        cell_properties=["Value", "RuleDerived"],
        elem_properties=["Type"],
        top=None)
    pp.pprint(raw_data)

    # default: (Case and space insensitive) dictionary
    data = tm1.cubes.cells.execute_mdx(mdx)
    print(data)
    # Note: can be converted into pandas dataframe with Utility function:
    df = Utils.build_pandas_dataframe_from_cellset(data, multiindex=False)
    pp.pprint(df)

    # values: get only the cell values
    values = tm1.cubes.cells.execute_mdx_values(mdx)
    for value in values:
        print(value)

    # csv: get cellset content as raw csv (Zero / null is suppressed by default, Context dimensions are omitted)
    csv = tm1.cubes.cells.execute_mdx_csv(mdx)
    print(csv)

    # dataframe: get cellset content as pandas dataframe (Zero / null is suppressed by default, Context dimensions are omitted)
    df = tm1.cubes.cells.execute_mdx_dataframe(mdx)
    print(df)

    # array
    array = tm1.cubes.cells.execute_mdx_ui_array(mdx, value_precision=1)
    pp.pprint(array)

    # dygraph
    dygraph = tm1.cubes.cells.execute_mdx_ui_dygraph(mdx, value_precision=1)
    pp.pprint(array)
