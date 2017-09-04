"""
Get private and public Subsets from TM1
"""

from TM1py.Services import TM1Service

with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:

    private_subsets = tm1.dimensions.subsets.get_all_names(dimension_name='plan_department',
                                                           hierarchy_name='plan_department',
                                                           private=True)
    print('private subsets: ')
    for subset_name in private_subsets:
        subset = tm1.dimensions.subsets.get(dimension_name='plan_department',
                                            subset_name=subset_name,
                                            private=True)
        print(subset.name)

    public_subsets = tm1.dimensions.subsets.get_all_names(dimension_name='plan_department',
                                                          hierarchy_name='plan_department',
                                                          private=False)
    print('public subsets: ')
    for subset_name in public_subsets:
        subset = tm1.dimensions.subsets.get(dimension_name='plan_department',
                                            subset_name=subset_name,
                                            private=False)
        print(subset.name)
