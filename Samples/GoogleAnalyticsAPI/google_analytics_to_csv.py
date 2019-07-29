"""Hello Analytics Reporting API V4."""

import csv
import json

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Credentials varibles
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'tm1-python-f785cd61dacd.json'
VIEW_ID = '149230861'
# Filename
FILE_NAME = 'google_analytics_data.csv'
RESPONSE_FILE_NAME = 'google_analytics_data.json'
# Google Analytics query
DATE_RANGE = [{'startDate': '7daysAgo', 'endDate': 'today'}]
METRICS = [{'expression': 'ga:sessions'}, {'expression': 'ga:sessionsPerUser'}, {'expression': 'ga:sessionDuration'},
           {'expression': 'ga:pageviews'}, {'expression': 'ga:bounces'}]
DIMENSIONS = [{'name': 'ga:date'}, {'name': 'ga:userType'}, {'name': 'ga:country'}, {'name': 'ga:region'},
              {'name': 'ga:city'}, {'name': 'ga:latitude'}, {'name': 'ga:longitude'}, {'name': 'ga:source'},
              {'name': 'ga:pageTitle'}]


def initialize_analytics_reporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics):
    """Queries the Analytics Reporting API V4.

    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
      The Analytics Reporting API V4 response.
    """
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': DATE_RANGE,
                    'metrics': METRICS,
                    'dimensions': DIMENSIONS
                }]
        }
    ).execute()


def print_response_to_json(response):
    for report in response.get('reports', []):
        with open(RESPONSE_FILE_NAME, 'w') as outfile:
            json.dump(report, outfile)


def generate_csv_headers(raw_dimension_headers, raw_metric_headers):
    headers = list()

    # Prepare headers
    for dimension_header in raw_dimension_headers:
        # remove the 'ga:'
        header = dimension_header[3:]
        headers.append(header)

    for metric_header in raw_metric_headers:
        # remove the 'ga:'
        header = metric_header.get('name')[3:]
        headers.append(header)

    return headers


def generate_csv_body(row):
    csv_row = []
    dimensions = row.get('dimensions', [])
    date_range_values = row.get('metrics', [])
    for dimension in dimensions:
        csv_row.append(dimension)
    for dateRangeValue in date_range_values[0].get('values', []):
        csv_row.append(dateRangeValue)
    return csv_row


def parse_response_to_csv_output(response):
    # Assumption: only one report in 'reports' key
    # ToDo: instead write multi report response into different files ?
    report = response.get('reports')[0]

    # Return empty list of google analytics response is lacking data
    # ToDo: Throw error instead ?
    if 'data' not in report:
        return []
    data = report.get('data')
    if 'rows' not in data:
        return []

    column_header = report.get('columnHeader', {})
    dimension_headers = column_header.get('dimensions', [])
    metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])

    # build csv headers
    csv_headers = generate_csv_headers(dimension_headers, metric_headers)

    # build csv body
    csv_body = []
    for row in report.get('data').get('rows'):
        csv_body.append(generate_csv_body(row))
    return [csv_headers] + csv_body


def print_to_csv(csv_output):
    with open(FILE_NAME, 'w', newline='') as report_csv:
        writer = csv.writer(report_csv, delimiter=";")
        writer.writerows(csv_output)


def main():
    # 1. Authenticate to Google Analytics
    analytics = initialize_analytics_reporting()
    # 2. Requests the data
    response = get_report(analytics)
    # 3. Print report into json format
    print_response_to_json(response)
    # 4. Print report into csv file
    csv_output = parse_response_to_csv_output(response)
    print_to_csv(csv_output)


if __name__ == '__main__':
    main()
