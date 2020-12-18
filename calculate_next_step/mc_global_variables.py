# please import this container as followed:
# import calculate_next_step.mc_global_variables as mc_globals
# mc stands for manuel calculated

# Python-libraries
import json

# Other modules from this project
# classes:
from data_classes.ManualCalculatedGame import ManualCalculatedGame

# contains prepared data of the game
simplified_game_class: ManualCalculatedGame
# Dict with the test-results
result: {str: [int, int]}
# How many moves (by our player) in que should be tested
# This variable starts by zero
test_depth: int
# List of all possible moves defined by the server
move_list: []


# this function must be called in main.py
def _init():
    json_dict = json.loads(open("./calculate_next_step/config.json", "r").read())
    global simplified_game_class
    simplified_game_class = None
    global test_depth
    test_depth = json_dict["test_depth"]
    global move_list
    move_list = json_dict["move_list"]
    global result
    result = {}
    for i in range(test_depth + 1):
        for move in move_list:
            result[move + "_" + str(i)] = [1, 1]
