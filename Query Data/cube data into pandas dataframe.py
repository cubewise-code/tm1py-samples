"""
- Query data from a cube view into a Pandas Dataframe.
http://pandas.pydata.org/

- Calculate statistical measures on dataset (mean, median, std)
"""


from TM1py.Services import TM1Service
from TM1py.Utils import Utils


with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:
    # define MDX Query
    mdx = "SELECT {[plan_time].[Jan-2004]:[plan_time].[Dec-2004]} * {[plan_chart_of_accounts].[Revenue]," \
                  "[plan_chart_of_accounts].[COS], [plan_chart_of_accounts].[Operating Expense], " \
                  "[plan_chart_of_accounts].[Net Operating Income]} on ROWS, "\
                  "{[plan_version].[FY 2004 Budget]} on COLUMNS  " \
            "FROM [plan_BudgetPlan] " \
            "WHERE ([plan_business_unit].[10110],[plan_department].[410], "\
                  "[plan_exchange_rates].[local],[plan_source].[input]) "

    # Get data from P&L cube through MDX
    pnl_data = tm1.cubes.cells.execute_mdx(mdx)

    # Build pandas DataFrame fram raw cellset data
    df = Utils.build_pandas_dataframe_from_cellset(pnl_data)

    print(df)

    # Calculate Std over Accounts
    print(df.groupby(level=3).std())

    # Calculate Mean over Accounts
    print(df.groupby(level=3).mean())

    # Calculate Median over Accounts
    print(df.groupby(level=3).median())

