"""
Query data through MDX

"""

from TM1py.Services import TM1Service


with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:
    # Define mdx query
    mdx = "SELECT " \
          "NON EMPTY {TM1SUBSETALL( [}Clients] )} on ROWS, " \
          "NON EMPTY {TM1SUBSETALL( [}Groups] )} ON COLUMNS " \
          "FROM [}ClientGroups]"

    # Get view content
    content = tm1.cubes.cells.execute_mdx(mdx)

    # Print content
    print(content)



