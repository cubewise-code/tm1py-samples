from TM1py import TM1Service


with TM1Service(address='localhost', port=8892, user='admin', password='apple', ssl=True, logging=True) as tm1:
    # path in TM1 Application-Tree
    path = 'Finance/P&L.xlsx'

    # get the application
    application = tm1.applications.get(path)

    # write it to xlsx file
    application.to_xlsx("out.xlsx")
