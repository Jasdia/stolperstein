# Python-libraries
from json import loads
from logging import info
from pathlib import Path

# The next action that will be performed by the bot.
action: str


# Resetting action after sending to server.
def reset_action():
    global action
    action = 'change_nothing'


# Checks how many moves where performed. Must be updated in action_play.py so that we know if we reached the 6th step
# (for the extra rule).
amount_of_moves: int
# How often should the bot retry to sent an answer to the server.
amount_of_retrying_sending_an_answer: int
# How many seconds should be subtracted from the deadline to answer the server.
answer_time_for_the_bot: int
# test_depth for mc
test_depth: int


# this function must only be called in main.py
def _init():
    _root_path = str(Path(__file__).parent.absolute())
    json_dict = loads(open(_root_path + "/config.json", "r").read())
    # Sets the default-value to 'change_nothing' in case the function is too slow.
    reset_action()
    # Sets the value to one, because the number will be changed after every move.
    global amount_of_moves
    amount_of_moves = 1
    global amount_of_retrying_sending_an_answer
    amount_of_retrying_sending_an_answer = json_dict['amount_of_retrying_sending_an_answer']
    global answer_time_for_the_bot
    answer_time_for_the_bot = json_dict['answer_time_for_the_bot']
    info("api_globals initialized.")
    global test_depth
    test_depth = json_dict['test_depth']
