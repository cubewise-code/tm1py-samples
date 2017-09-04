"""
Get a chore from TM1
"""

from TM1py.Services import TM1Service

# Connection to TM1 Server
with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:
    # Read Chore:
    c = tm1.chores.get('real chore')

    # Print out the tasks
    for task in c.tasks:
        print("Process: {} Parameters: {}".format(task, task.parameters))


