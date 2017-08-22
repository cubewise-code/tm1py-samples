"""
- Query data from a cube view into a Pandas Dataframe.
http://pandas.pydata.org/

- Calculate statistical measures on dataset (mean, median, std)
"""


import pandas as pd

from TM1py.Services import TM1Service
from TM1py.Utils import Utils


with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:
    # define MDX Query
    mdx = "SELECT {[plan_chart_of_accounts].[Revenue],[plan_chart_of_accounts].[COS], \
        [plan_chart_of_accounts].[Other Expenses],[plan_chart_of_accounts].[Payroll], \
        [plan_chart_of_accounts].[Travel],[plan_chart_of_accounts].[Operating Expense]} on ROWS, \
        {[plan_time].[Q1-2004],[plan_time].[Jan-2004],[plan_time].[Feb-2004],[plan_time].[Mar-2004]} on COLUMNS  \
    FROM [plan_BudgetPlan] \
    WHERE ([plan_version].[FY 2004 Budget],[plan_business_unit].[10110],[plan_department].[410], \
        [plan_exchange_rates].[local],[plan_source].[input]) "

    # Get data from P&L cube through MDX
    pnl_data = tm1.data.execute_mdx(mdx)

    # Build pandas DataFrame fram raw cellset data
    df = Utils.build_pandas_dataframe_from_cellset(pnl_data)

    # Calculate Std over Accounts
    print(df.groupby(level=3).std())

    # Calculate Mean over Accounts
    print(df.groupby(level=3).mean())

    # Calculate Median over Accounts
    print(df.groupby(level=3).median())

