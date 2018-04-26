""" 
- Create a cell annotation at a fix location in a cube.
- Get all annotations from a cube. 
- Delete the annotation that was created
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

import uuid

from TM1py.Services import TM1Service
from TM1py.Objects import Annotation

# connection to TM1 Server
tm1 = TM1Service(**config['tm1srv01'])

# just a random text
random_string = str(uuid.uuid4())

# create instance of TM1py.Annotation
a = Annotation(comment_value=random_string,
               object_name='plan_BudgetPlan',
               dimensional_context=['FY 2004 Forecast', '10110', '110', '61065', 'planning', 'revenue (future)',
                                    'Jan-2005'])

# create annotation on TM1 Server
tm1.cubes.annotations.create(a)

# find the created annotation and delete it
for annotation in tm1.cubes.annotations.get_all('plan_BudgetPlan'):
    if annotation.comment_value == random_string:
        tm1.cubes.annotations.delete(annotation_id=annotation.id)

# logout
tm1.logout()
