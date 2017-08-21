"""
Delete all private MDX Views

Important: MDXViews can not be seen in Architect/ Perspectives
"""


from TM1py.Objects import MDXView
from TM1py.Services import TM1Service


with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:
    private_views, public_views = tm1.views.get_all("Plan_BudgetPlan")
    for v in private_views:
        if isinstance(v, MDXView):
            tm1.views.delete(cube_name="Plan_BudgetPlan", view_name=v.name, private=True)




