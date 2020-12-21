# please import this container as followed:
# import api.api_feedback_global_variables as api_globals

# Python-libraries
import json
import logging

# Other modules from this project
# classes:
from data_classes.api.Game import Game

# This boolean records, if the next action of the bot is changed by some function so it can be posted.
# TODO("Deprecated?")
action_changed: bool
# The next action that will be performed by the bot.
action: str


# Resetting action after sending to server.
def reset_action():
    global action
    action = 'change_nothing'


# Checks how many moves where performed. Must be updated in action_play.py so that we know if we reached the 6th step
# (for the extra rule).
amount_of_moves: int
# Holds the object which contains the data received from the game-server.
game_as_class: Game
# How often should the bot retry to sent an answer to the server.
amount_of_retrying_sending_an_answer: int
# How many seconds should be subtracted from the deadline to answer the server.
answer_time_for_the_bot: int
# test_depth for mc
test_depth: int


# this function must only be called in main.py
def _init():
    json_dict = json.loads(open("./api/config.json", "r").read())
    # Sets the default-value to false since no function changed the next action.
    global action_changed
    action_changed = False
    # Sets the default-value to 'change_nothing' in case the function is too slow.
    reset_action()
    # Sets the value to one, because the number will be changed after every move.
    # TODO("Is 0 correct or should it be -1?")
    global amount_of_moves
    amount_of_moves = 1
    # Initializes the variable with none, because there is no data to create an object.
    global game_as_class
    game_as_class = None
    global amount_of_retrying_sending_an_answer
    amount_of_retrying_sending_an_answer = json_dict['amount_of_retrying_sending_an_answer']
    global answer_time_for_the_bot
    answer_time_for_the_bot = json_dict['answer_time_for_the_bot']
    logging.info("api_globals initialized.")
    global test_depth
    test_depth = json_dict['test_depth']
