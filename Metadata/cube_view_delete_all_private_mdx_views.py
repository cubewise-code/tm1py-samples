"""
Delete all private MDX Views
Important: MDXViews can not be seen in Architect/ Perspectives
"""
import configparser

from TM1py.Objects import MDXView
from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

cube = "Retail"

with TM1Service(**config['tm1srv01']) as tm1:
    private_views, public_views = tm1.cubes.views.get_all(cube)
    for v in private_views:
        if isinstance(v, MDXView):
            tm1.cubes.views.delete(cube_name=cube, view_name=v.name, private=True)
