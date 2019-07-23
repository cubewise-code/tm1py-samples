# Google Analytics to TM1

The script **google_analytics_to_csv.py** will enable you to get data from Google Analytics into a CSV file which you can then upload into TM1 using TM1 processes.

### Prerequisites
1. Get credentials: Follow carefully the [Google Analytics API documentation](https://developers.google.com/analytics/devguides/config/mgmt/v3/quickstart/service-py) to download your credentials
1. Once the json file with your credentials downloaded:
    * Do not forget to add the "client_email" from the .json file into your Google Analytics users list, this new user needs to have access to your Google analytics data
     "client_email": "send-data-to-tm1@tm1-python.iam.gserviceaccount.com",****
     * Update the KEY_FILE_LOCATION = 'newFile.json' in the script
1. Download and run the **HelloAnalytics.py** script (downloaded from the [Google Analytics API documentation](https://developers.google.com/analytics/devguides/config/mgmt/v3/quickstart/service-py)) to make sure your credentials are correct.
1. Once your credentials are correct, you can choose the right combinations of dimensions and metrics following the [Googlge Dimensions and Metrics Explorer](https://ga-dev-tools.appspot.com/dimensions-metrics-explorer/)

### Requirement:
Before running the script you will to install the following two libraries
* **Google Client librabry**: pip install --upgrade google-api-python-client
* **Client library for OAuth 2.0.**: pip install oauth2client

### Handling errors
If you get errors running this script, check the last line of the error message, this is where you will find the most meaningful information.