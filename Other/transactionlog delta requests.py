import time

from TM1py import TM1Service


with TM1Service(address='localhost', port=12354, user='admin', password='apple', ssl=True) as tm1:

    # Start Change Tracking
    tm1.server.initialize_transaction_log_delta_requests("Cube eq 'c2'")

    # Continuous checks
    def job():
        entries = tm1.server.execute_transaction_log_delta_request()
        if len(entries) > 0:
            for entry in entries:
                print(entry["Tuple"], entry["NewValue"])

    while True:
        job()
        time.sleep(1)
