# Python-libraries
from requests import get
from os import getenv


# Gets time from time-server.
# TODO("Get the code running!")
def get_server_time():
    actual_time = get(getenv('TIME'))
    print(actual_time)
    return actual_time
