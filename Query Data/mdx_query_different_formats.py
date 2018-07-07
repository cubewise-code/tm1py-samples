"""
Query a default TM1 "Planning Sample" server and show results in different formats
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

import pprint
import json
import inspect

from TM1py.Services import TM1Service

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
    mdx3 = """
        SELECT
        NON EMPTY {[plan_time].[Q1-2004],[plan_time].[Q2-2004],[plan_time].[Q3-2004],[plan_time].[Q4-2004]} on COLUMNS,
        NON EMPTY {[plan_chart_of_accounts].[Revenue],[plan_chart_of_accounts].[Net Operating Income]} on ROWS,
        NON EMPTY {[plan_business_unit].[Europe],[plan_business_unit].[North America] } on PAGES
        FROM [plan_Report]
        WHERE (
            [plan_department].[Total Organization],
            [plan_exchange_rates].[actual],
            [plan_report].[Budget]
            )
        """

    pp = pprint.PrettyPrinter(indent=2)

    for query in [mdx,mdx3]:
        print('MDX Query:')
        print(query)
        # Create view content
        cellset_id = tm1.cubes.cells.create_cellset(query)
        try:

            for format in ['raw', 'default', 'values', 'csv', 'dataframe', 'array', 'dygraph']:
                result = tm1.cubes.cells.extract_cellset(cellset_id, format=format )
                print("{} output format".format(format))
                pp.pprint( list(result) if inspect.isgenerator(result) else result )
                print()

        finally:
            tm1.cubes.cells.delete_cellset(cellset_id)

        print()
