# please import this container as followed:
# import neuronal_network.nn_global_variables as nn_globals

from data_classes.neural_network.SimpleGame import SimpleGame

simplified_game_class: SimpleGame
dead_players: list


# this function must be called in main.py
def _init():
    global simplified_game_class
    simplified_game_class = None
    global dead_players
    dead_players = []
