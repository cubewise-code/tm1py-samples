import configparser
from datetime import date, timedelta

import dateutil.parser
import numpy as np
import pandas as pd
import requests
from TM1py.Objects import Element, Dimension, Hierarchy, Cube, ElementAttribute, Subset, AnonymousSubset, \
    ViewAxisSelection, ViewTitleSelection, NativeView
from TM1py.Services import TM1Service
from TM1py.Utils.Utils import CaseAndSpaceInsensitiveTuplesDict


def build_date_dimension(tm1, dimension_name, first_date, last_date, overwrite):
    date_span = last_date - first_date
    dates = [str(first_date + timedelta(day)) for day in range(date_span.days + 1)]
    # Build Leaves
    leaves = [Element(name=date, element_type='Numeric') for date in dates]

    # Build Consolidations
    years = [str(year) for year in range(first_date.year, last_date.year + 1)]
    consolidations = [Element(name=year, element_type='Consolidated') for year in years]

    for year in years:
        for month in range(1, 13):
            year_month = year + "-" + str(month).zfill(2)
            consolidations.append(Element(name=year_month, element_type="Consolidated"))

    # Build Elements
    elements = leaves + consolidations

    # Build Edges
    edges = CaseAndSpaceInsensitiveTuplesDict()
    for year in years:
        for month in range(1, 13):
            year_month = year + "-" + str(month).zfill(2)
            edges[(year, year_month)] = 1
        for date in filter(lambda d: d[0:4] == year, dates):
            year_month = date[0:7]
            edges[(year_month, date)] = 1

    # Build Attribute
    attributes = [ElementAttribute('Alias', 'Alias'),
                  ElementAttribute('Year', 'String'),
                  ElementAttribute('Month', 'String'),
                  ElementAttribute('Day', 'String'),
                  ElementAttribute('Weekday', 'String')]

    # write Aliases
    attribute_values = {}
    for date in dates:
        # Year, Month, Day Attributes
        attribute_values[(date, 'Year')] = date.split('-')[0]
        attribute_values[(date, 'Month')] = date.split('-')[1]
        attribute_values[(date, 'Day')] = date.split('-')[2]
        attribute_values[(date, 'Weekday')] = dateutil.parser.parse(date).weekday() + 1
        # US Notation as Alias
        year, month, day = [str(int(ymd)) for ymd in date.split('-')]
        attribute_values[(date, 'Alias')] = month + "/" + day + "/" + year

    # Build Hierarchy, Dimension
    hier = Hierarchy(name=dimension_name, dimension_name=dimension_name, elements=elements, edges=edges,
                     element_attributes=attributes)
    dim = Dimension(name=dimension_name, hierarchies=[hier])

    # Interaction with TM1
    exists = tm1.dimensions.exists(dimension_name)
    if not exists:
        tm1.dimensions.create(dim)
    elif exists and overwrite:
        tm1.dimensions.update(dim)
    if not exists or overwrite:
        tm1.cubes.cells.write_values(cube_name="}ElementAttributes_" + dimension_name, cellset_as_dict=attribute_values)

    # Year Subsets
    for year in years:
        expr = "{ FILTER ( {TM1SubsetAll([Date])}, [Date].[Year] = '" + year + "' ) }"
        subset = Subset(year, dimension_name=dimension_name, hierarchy_name=dimension_name, expression=expr)
        if not tm1.dimensions.hierarchies.subsets.exists(year, dimension_name, dimension_name, private=False):
            tm1.dimensions.hierarchies.subsets.create(subset, private=False)
        else:
            tm1.dimensions.hierarchies.subsets.update(subset, private=False)


def build_simple_dimension(tm1, dimension_name, dimension_elements, overwrite):
    elements = [Element(name=element_name, element_type='Numeric')
                for element_name
                in dimension_elements]
    total_element = 'Total ' + dimension_name
    elements.append(Element(name=total_element, element_type='Consolidated'))

    edges = {(total_element, element): 1
             for element
             in dimension_elements}

    # Build Hierarchy, Dimension
    hier = Hierarchy(name=dimension_name, dimension_name=dimension_name, elements=elements, edges=edges)
    dim = Dimension(name=dimension_name, hierarchies=[hier])

    # Interaction with TM1
    exists = tm1.dimensions.exists(dimension_name)
    if not exists:
        tm1.dimensions.create(dim)
    elif exists and overwrite:
        tm1.dimensions.update(dim)


def build_cube(tm1, name, dimensions, rules=None, overwrite=False):
    cube = Cube(name, dimensions, rules=rules)
    exists = tm1.cubes.exists(name)
    if not exists:
        tm1.cubes.create(cube)
    if exists and overwrite:
        tm1.cubes.update(cube)


def load_data_chicago(tm1, cube_name):
    cellset = dict()
    with open("cubike_chicago.csv", "r") as file:
        for line_raw in file.readlines()[1:]:
            line = line_raw.split(',')
            cellset[('Actual', str(line[0]), 'Chicago', 'Count')] = line[1]
            cellset[('Actual', str(line[0]), 'Chicago', 'Seconds')] = line[2]
    # Send to TM1
    tm1.cubes.cells.write_values(cube_name, cellset)


def load_data_nyc(tm1, cube_name):
    cellset = dict()
    with open("cubike_nyc.csv", "r") as file:
        for line_raw in file.readlines()[1:]:
            line = line_raw.split(',')
            cellset[('Actual', str(line[0]), 'NYC', 'Count')] = line[1]
            cellset[('Actual', str(line[0]), 'NYC', 'Seconds')] = line[2]
    # Send to TM1
    tm1.cubes.cells.write_values(cube_name, cellset)


def load_data_washington_dc(tm1, cube_name):
    cellset = dict()
    with open("cubike_washington_dc.csv", "r") as file:
        for line_raw in file.readlines()[1:]:
            line = line_raw.split(',')
            cellset[('Actual', str(line[0]), 'Washington', 'Count')] = line[1]
            cellset[('Actual', str(line[0]), 'Washington', 'Seconds')] = line[2]
    # Send to TM1
    tm1.cubes.cells.write_values(cube_name, cellset)


def load_weather_data(tm1, station_city_mapping, weather_cube_name):
    # cellset for TM1
    cellset = dict()

    from_to_pairs = [
        ('2014-01-01', '2014-06-30'),
        ('2014-07-01', '2014-12-31'),
        ('2015-01-01', '2015-06-30'),
        ('2015-07-01', '2015-12-31'),
        ('2016-01-01', '2016-06-30'),
        ('2016-07-01', '2016-12-31'),
        ('2017-01-01', '2017-06-30'),
        ('2017-07-01', '2017-12-31')
    ]

    # Query data frm NOAA (no more than 1000 records per query allowed)
    for station in station_city_mapping.keys():
        for from_to in from_to_pairs:
            url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?' \
                  'datasetid=GHCND&' \
                  'startdate=' + from_to[0] + '&' \
                  'enddate=' + from_to[1] + '&' \
                  'limit=1000&' \
                  'datatypeid=TMIN&' \
                  'datatypeid=TAVG&' \
                  'datatypeid=TMAX&' \
                  'stationid=' + station
            headers = {"token": 'yyqEBOAbHVbtXkfAmZuPNfnSXvdfyhgn'}
            response = requests.get(url, headers=headers).json()
            results = response["results"]

            # Populate cellset from records
            for record in results:
                coordinates = (
                    'Actual',
                    record['date'][0:10],
                    station_city_mapping[record['station']],
                    record['datatype']
                )
                cellset[coordinates] = record['value'] / 10

    # send cellset to TM1
    tm1.cubes.cells.write_values(weather_cube_name, cellset)


def write_public_holidays_to_cube(tm1, cube_name):
    city_hierarchy = tm1.dimensions.hierarchies.get("city", "city")
    cities = [element.name for element in city_hierarchy if str(element.element_type) != 'Consolidated']
    cellset = dict()
    with open("cubike_public_holidays.csv", "r") as file:
        for row in file:
            _, date, name = row.split(',')
            for city in cities:
                cellset[(date, city, 'Public Holiday')] = 1
    tm1.cubes.cells.write_values(cube_name, cellset)


def build_views(tm1, overwrite):
    # build views in Bike Shares Cube
    cube_name = "Bike Shares"
    view_name = "2014 to 2017 Counts by Day"
    rows = [ViewAxisSelection('Date', AnonymousSubset('Date', 'Date', '{[Date].[2014-01-01]:[Date].[2017-12-31]}'))]
    columns = [ViewAxisSelection('City', AnonymousSubset('City', 'City', '{[City].[NYC], [City].[Chicago], [City].[Washington]}'))]
    titles = [ViewTitleSelection('Bike Shares Measure', AnonymousSubset('Bike Shares Measure', 'Bike Shares Measure', '{[Bike Shares Measure].[Count]}'), 'Count'),
              ViewTitleSelection('Version', subset=AnonymousSubset('Version', 'Version', elements=['Actual']), selected='Actual')]
    view = NativeView(cube_name, view_name, rows=rows, columns=columns, titles=titles, format_string="####.##")
    if tm1.cubes.views.exists(cube_name, view_name)[1]:
        if overwrite:
            tm1.cubes.views.update(view, False)
    else:
        tm1.cubes.views.create(view, private=False)
    view_name = "2017 Counts by Month"
    rows = [ViewAxisSelection('Date', AnonymousSubset('Date', 'Date', '{[Date].[2017-01]:[Date].[2017-12]}'))]
    columns = [ViewAxisSelection('City', AnonymousSubset('City', 'City', '{[City].[NYC], [City].[Chicago], [City].[Washington]}'))]
    titles = [ViewTitleSelection('Bike Shares Measure', AnonymousSubset('Bike Shares Measure', 'Bike Shares Measure', '{[Bike Shares Measure].[Count]}'), 'Count'),
              ViewTitleSelection('Version', subset=AnonymousSubset('Version', 'Version', elements=['Actual']), selected='Actual')]
    view = NativeView(cube_name, view_name, rows=rows, columns=columns, titles=titles, format_string="####.##")
    if tm1.cubes.views.exists(cube_name, view_name)[1]:
        if overwrite:
            tm1.cubes.views.update(view, False)
    else:
        tm1.cubes.views.create(view, private=False)

    # build views in Weather Data Cube
    cube_name = "Weather Data"
    view_name = "2014 to 2017 Average by Day"
    rows = [ViewAxisSelection('Date', AnonymousSubset('Date', 'Date', '{[Date].[2014-01-01]:[Date].[2017-12-31]}'))]
    columns = [ViewAxisSelection('City', AnonymousSubset('City', 'City', '{[City].[NYC], [City].[Chicago], [City].[Washington]}'))]
    titles = [ViewTitleSelection('Weather Data Measure', AnonymousSubset('Weather Data Measure', 'Weather Data Measure', '{[Weather DataMeasure].[TAVG]}'), 'TAVG'),
              ViewTitleSelection('Version', subset=AnonymousSubset('Version', 'Version', elements=['Actual']), selected='Actual')]
    view = NativeView(cube_name, view_name, rows=rows, columns=columns, titles=titles, format_string="####.##")
    if tm1.cubes.views.exists(cube_name, view_name)[1]:
        if overwrite:
            tm1.cubes.views.update(view, False)
    else:
        tm1.cubes.views.create(view, private=False)


def main(tm1):
    version_dimension_name = 'Version'
    version_dimension_elements = ('Actual', 'Detailed Forecast', 'Prophet Forecast')
    build_simple_dimension(tm1, version_dimension_name, version_dimension_elements, overwrite=True)
    # Create Default Subset
    subset = Subset('Default', version_dimension_name, version_dimension_name, elements=version_dimension_elements)
    if not tm1.dimensions.hierarchies.subsets.exists(subset_name=subset.name,
                                                     dimension_name=subset.dimension_name,
                                                     hierarchy_name=subset.dimension_name,
                                                     private=False):
        tm1.dimensions.hierarchies.subsets.create(subset, private=False)
    else:
        tm1.dimensions.hierarchies.subsets.update(subset, private=False)

    measure_dimension_name = 'Bike Shares Measure'
    measure_dimension_elements = ('Count', 'Count Lower', 'Count Upper', 'Seconds', 'Minutes', 'Hours', 'Days')
    build_simple_dimension(tm1, measure_dimension_name, measure_dimension_elements, overwrite=True)
    # Create Default Subset
    subset = Subset('Default', measure_dimension_name, measure_dimension_name, elements=measure_dimension_elements)
    if not tm1.dimensions.hierarchies.subsets.exists(subset_name=subset.name,
                                                     dimension_name=subset.dimension_name,
                                                     hierarchy_name=subset.dimension_name,
                                                     private=False):
        tm1.dimensions.hierarchies.subsets.create(subset, private=False)
    else:
        tm1.dimensions.hierarchies.subsets.update(subset, private=False)

    city_dimension_name = 'City'
    city_dimension_elements = ('Chicago', 'NYC', 'Washington')
    build_simple_dimension(tm1, city_dimension_name, city_dimension_elements, overwrite=True)
    # Create Default Subset
    subset = Subset('Default', city_dimension_name, city_dimension_name, elements=city_dimension_elements)
    if not tm1.dimensions.hierarchies.subsets.exists(subset_name=subset.name,
                                                     dimension_name=subset.dimension_name,
                                                     hierarchy_name=subset.dimension_name,
                                                     private=False):
        tm1.dimensions.hierarchies.subsets.create(subset, private=False)
    else:
        tm1.dimensions.hierarchies.subsets.update(subset, private=False)

    date_dimension_name = 'Date'
    first_date = date(2010, 1, 1)
    last_date = date(2025, 12, 31)
    build_date_dimension(tm1, date_dimension_name, first_date, last_date, overwrite=True)

    # Build Bike Shares Cube
    cube_name = 'Bike Shares'
    dimensions = (version_dimension_name, date_dimension_name, city_dimension_name, measure_dimension_name)
    rules = "SKIPCHECK; \r\n" \
            "['Bike Shares Measure':'Minutes'] = N: ['Bike Shares Measure':'Seconds'] / 60; \r\n" \
            "['Bike Shares Measure':'Hours'] = N: ['Bike Shares Measure':'Seconds'] / (60 * 60); \r\n" \
            "['Bike Shares Measure':'Days'] = N: ['Bike Shares Measure':'Seconds'] / (60 * 60 * 24); \r\n" \
            "FEEDERS; \r\n" \
            "['Bike Shares Measure':'Seconds'] =>['Bike Shares Measure':'Minutes']; \r\n" \
            "['Bike Shares Measure':'Seconds'] =>['Bike Shares Measure':'Hours']; \r\n" \
            "['Bike Shares Measure':'Seconds'] => ['Bike Shares Measure':'Days']; \r\n"
    build_cube(tm1, cube_name, dimensions, rules=rules, overwrite=True)

    # Build Weather Cube
    weather_measure_element_names = ("TMAX", "TMIN", 'TAVG')
    weather_measure_dimension = 'Weather Data Measure'
    build_simple_dimension(tm1,
                           dimension_name=weather_measure_dimension,
                           dimension_elements=weather_measure_element_names,
                           overwrite=True)

    weather_cube_name = 'Weather Data'
    dimensions = (version_dimension_name, date_dimension_name, city_dimension_name, weather_measure_dimension)
    rules = "[] = C: IF ( DTYPE('Date', !Date) @= 'N' , \r\n" \
            "STET, \r\n" \
            "CONTINUE ); \r\n" \
            "['Weather Data Measure':'TMIN'] = C: ConsolidatedMin(1, 'Weather Data', !Version, !Date, !City, !Weather Data Measure);  \r\n" \
            "['Weather Data Measure':'TAVG'] = C: ConsolidatedAvg(1, 'Weather Data', !Version, !Date, !City, !Weather Data Measure);  \r\n" \
            "['Weather Data Measure':'TMAX'] = C: ConsolidatedMax(1, 'Weather Data', !Version, !Date, !City, !Weather Data Measure);"
    build_cube(tm1, weather_cube_name, dimensions, rules=rules, overwrite=True)

    # Build Holiday Measure Dimension
    holidays_measure_dimension_element_names = ("Public Holiday",)
    holidays_measure_dimension_name = 'Public Holidays Measure'
    build_simple_dimension(tm1,
                           dimension_name=holidays_measure_dimension_name,
                           dimension_elements=holidays_measure_dimension_element_names,
                           overwrite=True)

    # Build Holiday Cube
    holidays_cube_name = "Public Holidays"
    holidays_cube_dimensions = (date_dimension_name, city_dimension_name, holidays_measure_dimension_name)
    build_cube(tm1, holidays_cube_name, holidays_cube_dimensions, rules=None, overwrite=True)

    write_public_holidays_to_cube(tm1, holidays_cube_name)

    # build views
    build_views(tm1, overwrite=True)

    # Load Historic Weather
    station_city_mapping = {
        'GHCND:USW00014732': 'NYC',
        'GHCND:USW00094846': 'Chicago',
        'GHCND:USW00093721': 'Washington'
    }
    load_weather_data(tm1, station_city_mapping, weather_cube_name)

    # load raw Bike Shares data
    load_data_washington_dc(tm1, cube_name)
    load_data_chicago(tm1, cube_name)
    load_data_nyc(tm1, cube_name)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(r'..\..\config.ini')

    with TM1Service(**config['tm1srv01']) as tm1:
        main(tm1)
