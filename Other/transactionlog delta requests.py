import time

from TM1py import TM1Service

# TM1 Connection Parameters
source = {
    "address": '10.77.19.60',
    "port": 12354,
    "user": 'admin',
    "password": 'apple',
    "ssl": True,
    "cube": 'c1',
}

target = {
    "address": '10.77.19.60',
    "port": 9699,
    "user": 'admin',
    "password": 'apple',
    "ssl": False,
    "cube": 'c1',
}


# Establish connection to TM1 Source
with TM1Service(**source) as tm1_source:

    # Start Change Tracking
    tm1_source.server.initialize_transaction_log_delta_requests("Cube eq '" + source["cube"] + "'")

    # Continuous checks
    def job():
        entries = tm1_source.server.execute_transaction_log_delta_request()
        if len(entries) > 0:
            cellset = dict()
            for entry in entries:
                cellset[tuple(entry["Tuple"])] = entry["NewValue"]
            with TM1Service(**target) as tm1_target:
                tm1_target.cubes.cells.write_values(target["cube"], cellset)


    while True:
        job()
        time.sleep(1)
