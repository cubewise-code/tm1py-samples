"""
Query a default TM1 "Planning Sample" server and show results in different formats
"""

import pprint
import configparser

from TM1py.Services import TM1Service
from TM1py.Utils import Utils

# Read Config
config = configparser.ConfigParser()
config.read('./config.ini')

# Initializer Prettyprinter
pp = pprint.PrettyPrinter(indent=2)

# Connect to TM1
with TM1Service(**config['tm1srv01']) as tm1:

    def query_formats(
            mdx,
            cell_properties=None,
            elem_properties=None,
            member_properties=None,
            value_precision=None,
            top=None):

        print("Query:")
        print(mdx)

        # raw: native response dictionary
        print("\nRaw (native) format")
        raw_data = tm1.cubes.cells.execute_mdx_raw(
            mdx=mdx,
            cell_properties=cell_properties,
            elem_properties=elem_properties,
            member_properties=member_properties,
            top=None)
        pp.pprint(raw_data)

        # default: (Case and space insensitive) dictionary
        print("\nDefault: (Case and space insensitive) dictionary")
        data = tm1.cubes.cells.execute_mdx(mdx,cell_properties=cell_properties)
        print(data)
        # Note: can be converted into pandas dataframe with Utility function:
        print("\nCoverted to dataframe")
        df = Utils.build_pandas_dataframe_from_cellset(data, multiindex=False)
        pp.pprint(df)

        # values: get only the cell values
        print("\nValues only")
        values = tm1.cubes.cells.execute_mdx_values(mdx)
        for value in values:
            print(value)

        # csv: get cellset content as raw csv (Zero / null is suppressed by default, Context dimensions are omitted)
        print("\nCSV")
        csv = tm1.cubes.cells.execute_mdx_csv(mdx)
        print(csv)

        # dataframe: get cellset content as pandas dataframe (Zero / null is suppressed by default, Context dimensions are omitted)
        print("\ndataframe (pandas)")
        df = tm1.cubes.cells.execute_mdx_dataframe(mdx)
        print(df)

        # array
        print("\nArray: for grids and charts")
        array = tm1.cubes.cells.execute_mdx_ui_array(
            mdx=mdx, 
            value_precision=value_precision,
            elem_properties=elem_properties,
            member_properties=member_properties)
        pp.pprint(array)

        # dygraph
        print("\nDygraph: for charts that want columns of data, instead of rows")
        dygraph = tm1.cubes.cells.execute_mdx_ui_dygraph(
            mdx=mdx, 
            value_precision=value_precision,
            elem_properties=elem_properties,
            member_properties=member_properties)
        pp.pprint(dygraph)



    # Sample query from TM1 sample server called "Planning Sample"
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

    # Calculated member 
    # mdx = """
    #     WITH MEMBER [plan_time].[H1-2004] AS [plan_time].[Q1-2004] + [plan_time].[Q2-2004]
    #     SELECT
    #     NON EMPTY {[plan_time].[H1-2004],[plan_time].[Q3-2004],[plan_time].[Q4-2004]} on COLUMNS,
    #     NON EMPTY {[plan_chart_of_accounts].[Revenue],[plan_chart_of_accounts].[Net Operating Income]} on ROWS
    #     FROM [plan_Report]
    #     WHERE (
    #         [plan_business_unit].[Total Business Unit], 
    #         [plan_department].[Total Organization],
    #         [plan_exchange_rates].[actual],
    #         [plan_report].[Budget]
    #         )
    #     """

    # Calculated member and stacked row header
    # mdx = """
    #     WITH MEMBER [plan_time].[H1-2004] AS [plan_time].[Q1-2004] + [plan_time].[Q2-2004]
    #     SELECT
    #     NON EMPTY {[plan_time].[H1-2004],[plan_time].[Q3-2004],[plan_time].[Q4-2004]} on COLUMNS,
    #     NON EMPTY { {[plan_business_unit].[Total Business Unit]} * {[plan_chart_of_accounts].[Revenue],[plan_chart_of_accounts].[Net Operating Income]} } on ROWS
    #     FROM [plan_Report]
    #     WHERE (
    #         [plan_department].[Total Organization],
    #         [plan_exchange_rates].[actual],
    #         [plan_report].[Budget]
    #         )
    #     """

    # 3-Dimensional query
    # mdx = """
    #     SELECT
    #     NON EMPTY {[plan_time].[Q1-2004],[plan_time].[Q2-2004],[plan_time].[Q3-2004],[plan_time].[Q4-2004]} on COLUMNS,
    #     NON EMPTY {[plan_chart_of_accounts].[Revenue],[plan_chart_of_accounts].[Net Operating Income]} on ROWS,
    #     NON EMPTY {[plan_business_unit].[Europe],[plan_business_unit].[North America] } on PAGES
    #     FROM [plan_Report]
    #     WHERE (
    #         [plan_department].[Total Organization],
    #         [plan_exchange_rates].[actual],
    #         [plan_report].[Budget]
    #         )
    #     """

    query_formats(
            mdx=mdx,
            cell_properties=["Value","FormattedValue","RuleDerived"],
            elem_properties=None,#["Name","Type","Index"],
            member_properties=["Name"],#,"UniqueName","Attributes"],
            top=None)
