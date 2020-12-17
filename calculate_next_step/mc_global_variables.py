# please import this container as followed:
# import calculate_next_step.mc_global_variables as mc_globals
# mc stands for manuel calculated

# Other modules from this project
# classes:
from data_classes.ManualCalculatedGame import ManualCalculatedGame

# contains prepared data of the game
simplified_game_class: ManualCalculatedGame
# Dict with the test-results
result: {str: [int, int]}
# How many moves (by our player) in que should be tested
test_depth: int


# this function must be called in main.py
def _init():
    global simplified_game_class
    simplified_game_class = None
    global result
    result = {
        'turn_left': [0, 0],
        'turn_right': [0, 0],
        'slow_down': [0, 0],
        'speed_up': [0, 0],
        'change_nothing': [0, 0]
    }
    global test_depth
    test_depth = 2
