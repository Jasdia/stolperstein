# please import this container as followed:
# import api.api_feedback_global_variables as api_globals

# Other modules from this project
# classes:
from data_classes.api.Game import Game

# This boolean records, if the next action of the bot is changed by some function so it can be posted.
# TODO("Deprecated?")
action_changed: bool
# The next action that will be performed by the bot.
action: str
# Checks how many moves where performed. Must be updated in action_play.py so that we know if we reached the 6th step
# (for the extra rule).
amount_of_moves: int
# Holds the object which contains the data received from the game-server.
game_as_class: Game


# this function must only be called in main.py
def _init():
    # Sets the default-value to false since no function changed the next action.
    global action_changed
    action_changed = False
    # Sets the default-value to 'change_nothing' in case the function is too slow.
    global action
    action = 'change_nothing'
    # Sets the value to zero, because no move is done yet.
    # TODO("Is 0 correct or should it be -1?")
    global amount_of_moves
    amount_of_moves = 0
    # Initializes the variable with none, because there is no data to create an object.
    global game_as_class
    game_as_class = None
