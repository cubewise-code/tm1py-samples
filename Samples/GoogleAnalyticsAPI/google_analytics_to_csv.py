"""Hello Analytics Reporting API V4."""

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json
import csv

# Credentials varibles
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'tm1-python-f785cd61dacd.json'
VIEW_ID = '149230861'
# Filename
file_name = 'google_analytics_data.csv'
response_file_name = 'google_analytics_data.json'
# Google Analytics query
date_ranges = [{'startDate': '7daysAgo', 'endDate': 'today'}]
metrics = [{'expression': 'ga:sessions'}, {'expression': 'ga:sessionsPerUser'}, {'expression': 'ga:sessionDuration'},{'expression': 'ga:pageviews'}, {'expression': 'ga:bounces'}]
dimensions = [{'name': 'ga:date'}, {'name': 'ga:userType'}, {'name': 'ga:country'}, {'name': 'ga:region'},{'name': 'ga:city'}, {'name': 'ga:latitude'}, {'name': 'ga:longitude'}, {'name': 'ga:source'},{'name': 'ga:pageTitle'}]


def initialize_analyticsreporting():
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
          'dateRanges': date_ranges,
          'metrics': metrics,
          'dimensions': dimensions
        }]
      }
  ).execute()

def print_response_to_json(response):
  for report in response.get('reports', []):
    with open(response_file_name, 'w') as outfile:
      json.dump(report, outfile)

def print_response_to_csv(response):
  """Parses and prints the Analytics Reporting API V4 response.
  Args:
    response: An Analytics Reporting API V4 response.
  """
  csvOutput = []
  csvHeaders = []
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    #Prepare headers
    for dimensionHeader in dimensionHeaders:
      # remove the 'ga:'
      header = dimensionHeader[3:len(dimensionHeader)]
      csvHeaders.append(header)

    for metricHeader in metricHeaders:
      # remove the 'ga:'
      header = metricHeader.get('name')[3:len(metricHeader.get('name'))]
      csvHeaders.append(header)

    #Headers ready
    csvOutput.append(csvHeaders)

    # Row data
    for row in report.get('data', {}).get('rows', []):
      csvRow = []
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])
      for dimension in dimensions:
        csvRow.append(dimension)
      for dateRangeValue in dateRangeValues[0].get('values', []):
        csvRow.append(dateRangeValue)
      csvOutput.append(csvRow)

    # Output csv with the results
    reportCsv = open(file_name, 'w', newline='')
    with reportCsv:
      writer = csv.writer(reportCsv, delimiter=";")
      for row in csvOutput:
        writer.writerow(row)

def main():
  #1. Authenticate to Google Analytics
  analytics = initialize_analyticsreporting()
  #2. Requests the data
  response = get_report(analytics)
  #3. Print report into json format
  print_response_to_json(response)
  #3 bit Print report into csv file
  print_response_to_csv(response)

if __name__ == '__main__':
  main()