import requests
import os


def get_server_time():
    actual_time = requests.get(os.getenv('TIME'))
    print(actual_time)
    return actual_time
