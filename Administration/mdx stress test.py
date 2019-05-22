"""
Do MDX Queries asynchronously. 
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

import asyncio

from TM1py.Services import TM1Service

# mdx Queries
mdx1 = "SELECT {[plan_version].MEMBERS}*{[plan_chart_of_accounts].Members} * {[plan_exchange_rates].Members}  on COLUMNS, {[plan_business_unit].MEMBERS}*{[plan_department].MEMBERS} on ROWS FROM [plan_BudgetPlan]WHERE ([plan_source].[input], [plan_time].[Jun-2004] )"
mdx2 = "SELECT {[plan_version].MEMBERS}*{[plan_chart_of_accounts].Members} * {[plan_exchange_rates].Members}  on COLUMNS, {[plan_business_unit].MEMBERS}*{[plan_department].MEMBERS} on ROWS FROM [plan_BudgetPlan]WHERE ([plan_source].[input], [plan_time].[Jun-2004] )"
mdx3 = "SELECT {[plan_version].MEMBERS}*{[plan_chart_of_accounts].Members} * {[plan_exchange_rates].Members}  on COLUMNS, {[plan_business_unit].MEMBERS}*{[plan_department].MEMBERS} on ROWS FROM [plan_BudgetPlan]WHERE ([plan_source].[input], [plan_time].[Jun-2004] )"
mdx4 = "SELECT {[plan_version].MEMBERS}*{[plan_chart_of_accounts].Members} * {[plan_exchange_rates].Members}  on COLUMNS, {[plan_business_unit].MEMBERS}*{[plan_department].MEMBERS} on ROWS FROM [plan_BudgetPlan]WHERE ([plan_source].[input], [plan_time].[Jun-2004] )"
mdx5 = "SELECT {[plan_version].MEMBERS}*{[plan_chart_of_accounts].Members} * {[plan_exchange_rates].Members}  on COLUMNS, {[plan_business_unit].MEMBERS}*{[plan_department].MEMBERS} on ROWS FROM [plan_BudgetPlan]WHERE ([plan_source].[input], [plan_time].[Jun-2004] )"


# Define function
def execute_mdx(tm1, mdx):
    for i in range(10):
        tm1.cubes.cells.execute_mdx(mdx)

# Fire requests asynchronously
async def main():
    loop = asyncio.get_event_loop()
    with TM1Service(**config['tm1srv01']) as tm1:

        future1 = loop.run_in_executor(None, execute_mdx, tm1, mdx1)
        future2 = loop.run_in_executor(None, execute_mdx, tm1, mdx2)
        future3 = loop.run_in_executor(None, execute_mdx, tm1, mdx3)
        future4 = loop.run_in_executor(None, execute_mdx, tm1, mdx4)
        future5 = loop.run_in_executor(None, execute_mdx, tm1, mdx5)
        response1, response, response3, response4, response5 = \
            await future1, await future2, await future3, await future4, await future5


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
