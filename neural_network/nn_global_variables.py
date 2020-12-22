# please import this container as followed:
# import neural_network.nn_global_variables as nn_globals

from data_classes.neural_network.SimpleGame import SimpleGame
from deprecated import deprecated

simplified_game_class: SimpleGame
dead_players: list


# this function must be called in main.py
@deprecated(reason="Probably oversize!")
def _init():
    global simplified_game_class
    simplified_game_class = None
    global dead_players
    dead_players = []
