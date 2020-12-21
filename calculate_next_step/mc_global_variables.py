# please import this container as followed:
# import calculate_next_step.mc_global_variables as mc_globals
# mc stands for manuel calculated

# Python-libraries
import json
import logging


# Dict with the test-results
result: {str: [int, int]}
# List of all possible moves defined by the server
move_list: []


# this function must be called in main.py
def _init():
    json_dict = json.loads(open("./calculate_next_step/config.json", "r").read())
    global move_list
    move_list = json_dict["move_list"]
    global result
    result = {}
    for move in move_list:
        result[move] = [0, 0]
    logging.info("mc_globals initialized.")
