"""
Get private and public Subsets from TM1
"""

from TM1py.Services import TM1Service

with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:

    private_subsets = tm1.subsets.get_all_names('plan_department', 'plan_department', True)
    print('private subsets: ')
    for subset_name in private_subsets:
        subset = tm1.subsets.get('plan_department', subset_name, True)
        print(subset.name)

    public_subsets = tm1.subsets.get_all_names('plan_department', 'plan_department', False)
    print('public subsets: ')
    for subset_name in public_subsets:
        subset = tm1.subsets.get('plan_department', subset_name, False)
        print(subset.name)
