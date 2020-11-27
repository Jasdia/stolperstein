# please import this container as followed:
# import api.api_feedback_global_variables as api_globals

from data_classes.Game import Game

action_changed: bool
action: str
amount_of_moves: int
game_as_class: Game


# this function must be called in main.py
def init():
    global action_changed
    action_changed = 'true'
    global action
    action = 'change_nothing'
    global amount_of_moves
    amount_of_moves = 0
    global game_as_class
    game_as_class = None
