# please import this container as followed:
# import calculate_next_step.mc_global_variables as mc_globals
# mc stands for manuel calculated

from data_classes.ManualCalculatedGame import ManualCalculatedGame

simplified_game_class: ManualCalculatedGame
result: {str: [int, int]}


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
