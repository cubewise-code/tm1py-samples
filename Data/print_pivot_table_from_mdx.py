import configparser

from TM1py import TM1Service, NativeView, AnonymousSubset

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

mdx = """
SELECT
NON EMPTY {[Date].[2017-11-26], [Date].[2017-11-27]} * {[Bike Shares Measure].[Count]} ON ROWS,
NON EMPTY {[City].[NYC], [City].[Chicago]} ON COLUMNS
FROM [Bike Shares]
WHERE ([Version].[Actual])
"""

with TM1Service(**config['tm1srv01']) as tm1:
    pivot = tm1.cubes.cells.execute_mdx_dataframe_pivot(mdx=mdx)
    print(pivot)

view = NativeView(
    cube_name="Bike Shares",
    view_name="Bike Shares By City",
    suppress_empty_columns=True,
    suppress_empty_rows=True)
view.add_row(
    dimension_name="Date",
    subset=AnonymousSubset(
        dimension_name="Date",
        expression="{Tm1SubsetAll([Date])}"))
view.add_row(
    dimension_name="Bike Shares Measure",
    subset=AnonymousSubset(
        dimension_name="Bike Shares Measure",
        elements=["Count"]))
view.add_column(
    dimension_name="City",
    subset=AnonymousSubset(
        dimension_name="City",
        elements=["NYC", "Chicago"]))
view.add_title(
    dimension_name="Version",
    selection="Actual",
    subset=AnonymousSubset(
        dimension_name="Version",
        elements=["Actual"]))

with TM1Service(**config['tm1srv01']) as tm1:
    if tm1.cubes.views.exists(cube_name="Bike Shares", view_name="Bike Shares By City", private=False):
        tm1.cubes.views.delete(cube_name="Bike Shares", view_name="Bike Shares By City", private=False)

    tm1.cubes.views.create(
        view=view,
        private=False)

    pivot = tm1.cubes.cells.execute_view_dataframe_pivot(
        cube_name="Bike Shares",
        view_name="Bike Shares By City")

    print(pivot)
