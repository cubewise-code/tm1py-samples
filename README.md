<center><img src="https://s3-ap-southeast-2.amazonaws.com/downloads.cubewise.com/web_assets/CubewiseLogos/Final+logos_Samples.png" 
style="width: 80%; height: 80%;text-align: center"/></center>

TM1py Samples is a great starting point to get up to speed with TM1py. It contains 60+ ready-to-use TM1py scripts such as:

- load TM1 data into pandas for statistical analysis
- load FX, Stock and GDP data from external sources into your cubes
- synchronize cubes from different TM1 instances
- clean your TM1 models through regular expressions
- generate MDX Queries from existing cube views
- analyse Processing Feeders time
- maintain dimensions and subsets with python
- ...

All scripts are split into four categories:
* **Aministration**: All tasks related to TM1 administration such as sessions, transaction logs...
* **Data**: Data operation such as getting data out of a view or writing data back to TM1
* **Metadata**: All operations related to TM1 objects such as creating a new dimension, deleting a view...
* **Samples**: Groups more advanced scripts such as getting data from web services

# Requirements

- TM1       (10.2.2 FP 5 or higher)
- TM1py    [Installing TM1py guide](https://code.cubewise.com/tm1py-help-content/installing-tm1py)

# Usage

The first script you should run is **check.py** which enables you to check if TM1py can connect to your TM1 instance:
* [Check connectivity with TM1](https://code.cubewise.com/tm1py-help-content/check-connectivity-with-tm1)

To run a script from a command line, download the TM1py-samples repository, navigate to the script folder and then just use the command **python script_name.py**.
Python scripts can also be run from [TM1 processes](https://code.cubewise.com/tm1py-help-content/run-tm1py-script-from-tm1-process).

# Documentation about TM1py
* Help articles: https://code.cubewise.com/tm1py-help
* All TM1py functions: http://tm1py.readthedocs.io/en/latest/


# Other

## Python Tutorial

If you are not familiar with the Python programming language you might want to look into some basic tutorials,
before starting with TM1py.
thenewboston offers awesome (and free) Python tutorials on his Youtube Channel
https://www.youtube.com/watch?v=HBxCHonP6Ro

## IDE

PyCharm is likely the best IDE for Python. It offers intelligent code completion, on-the-fly error checking and heaps of other features.
It allows you to save time and be more productive.
JetBrains offers a free Community Edition of PyCharm
https://www.jetbrains.com/pycharm/


# Issues

If you find issues, sign up in Github and open an Issue in this repository

# Contribution

If you wrote cool sample scripts with TM1py, that might be useful for others, feel free to push them to this repository
