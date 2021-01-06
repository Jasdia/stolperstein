# Python-libraries
from json import loads
from logging import info
from pathlib import Path


# List of all possible moves defined by the server
move_list: []


# this function must be called in main.py
def _init():
    _root_path = str(Path(__file__).parent.absolute())
    file = open(_root_path + "/config.json", "r")
    json_dict = loads(file.read())
    file.close()
    global move_list
    move_list = json_dict["move_list"]
    info("mc_globals initialized.")
