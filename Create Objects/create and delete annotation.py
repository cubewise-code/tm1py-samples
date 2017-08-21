""" 
- Create a cell annotation at a certain location.
- Get all annotations from a cube. 
- Delete the annotation that was created

"""

import uuid

from TM1py.Services import TM1Service
from TM1py.Objects import Annotation

# connection to TM1 Server
tm1 = TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True)

# just a random text
random_string = str(uuid.uuid4())

# create instance of TM1py.Annotation
a = Annotation(comment_value=random_string,
               object_name='plan_BudgetPlan',
               dimensional_context=['FY 2004 Forecast', '10110', '110', '61065', 'planning', 'revenue (future)',
                                    'Jan-2005'])

# create annotation on TM1 Server
tm1.annotations.create(a)

# find the created annotation and delete it
for annotation in tm1.annotations.get_all('plan_BudgetPlan'):
    if annotation.comment_value == random_string:
        tm1.annotations.delete(annotation_id=annotation.id)

# logout
tm1.logout()
