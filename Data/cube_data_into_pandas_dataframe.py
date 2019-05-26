"""
- Query data from a cube view into a Pandas Dataframe.
http://pandas.pydata.org/

- Calculate statistical measures on dataset (mean, median, std)
"""
import configparser

from TM1py.Services import TM1Service
from TM1py.Utils import Utils

config = configparser.ConfigParser()
config.read(r'..\config.ini')

with TM1Service(**config['tm1srv01']) as tm1:
    # define MDX Query
    mdx = "SELECT {[plan_time].[Jan-2004]:[plan_time].[Dec-2004]} * {[plan_chart_of_accounts].[Revenue]," \
          "[plan_chart_of_accounts].[COS], [plan_chart_of_accounts].[Operating Expense], " \
          "[plan_chart_of_accounts].[Net Operating Income]} on ROWS, " \
          "{[plan_version].[FY 2004 Budget]} on COLUMNS  " \
          "FROM [plan_BudgetPlan] " \
          "WHERE ([plan_business_unit].[10110],[plan_department].[410], " \
          "[plan_exchange_rates].[local],[plan_source].[input]) "

    # Get data from P&L cube through MDX
    pnl_data = tm1.cubes.cells.execute_mdx(mdx)

    # Build pandas DataFrame fram raw cellset data
    df = Utils.build_pandas_dataframe_from_cellset(pnl_data)

    print(df)

    # Calculate Statistical measures for dataframe
    print(df.describe())
