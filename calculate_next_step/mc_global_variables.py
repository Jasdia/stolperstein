# Python-libraries
from json import loads
from logging import info
from pathlib import Path


# List of all possible moves defined by the server
move_list: []
# Saves the highest test_step
highest_test_step: int


def rest_highest_test_step():
    global highest_test_step
    highest_test_step = -1


# this function must be called in main.py
def _init():
    _root_path = str(Path(__file__).parent.absolute())
    json_dict = loads(open(_root_path + "/config.json", "r").read())
    global move_list
    move_list = json_dict["move_list"]
    rest_highest_test_step()
    info("mc_globals initialized.")
