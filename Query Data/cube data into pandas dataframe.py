"""
- Query data from a cube view into a Pandas Dataframe.
http://pandas.pydata.org/

- Calculate statistical measures on dataset (mean, median, std)
"""


import pandas as pd

from TM1py.Services import TM1Service
from TM1py import Utils


with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:
    # Get data from P&L cube
    pnl_data = tm1.data.get_view_content(cube_name='Plan_BudgetPlan',
                                         view_name='Budget Input Detailed',
                                         cell_properties=['Ordinal', 'Value'],
                                         private=False)

    # Build pandas DataFrame fram raw cellset data
    df = Utils.build_pandas_dataframe_from_cellset(pnl_data)

    # Calculate Std over Accounts
    print(df.groupby(level=3).std())

    # Calculate Mean over Accounts
    print(df.groupby(level=3).mean())

    # Calculate Median over Accounts
    print(df.groupby(level=3).median())

