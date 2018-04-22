"""
Delete all private MDX Views
Important: MDXViews can not be seen in Architect/ Perspectives
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from TM1py.Objects import MDXView
from TM1py.Services import TM1Service

cube = "Retail"

with TM1Service(**config['source']) as tm1:
    private_views, public_views = tm1.cubes.views.get_all(cube)
    for v in private_views:
        if isinstance(v, MDXView):
            tm1.cubes.views.delete(cube_name=cube, view_name=v.name, private=True)




