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
    global test_depth
    test_depth = 1
    global result
    tmp_move_list = ['turn_left', 'turn_right', 'slow_down', 'speed_up', 'change_nothing']
    result = {}
    for i in range(test_depth):
        for move in tmp_move_list:
            result[move + "_" + str(i)] = [0, 0]
    print(result)