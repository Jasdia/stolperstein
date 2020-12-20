# Python-libraries
import requests
import os


# Gets time from time-server.
# TODO("Get the code running!")
def get_server_time():
    actual_time = requests.get(os.getenv('TIME'))
    print(actual_time)
    return actual_time
