import requests
import os

server_time = requests.get(os.getenv('TIME'))
