# Python-libraries
from json import loads
from logging import info
from pathlib import Path

# How often should the bot retry to sent an answer to the server.
amount_of_retrying_sending_an_answer: int
# How many seconds should be subtracted from the deadline to answer the server.
answer_time_for_the_bot: int
# test_depth for mc
test_depth: int


# this function must only be called in main.py
def _init():
    _root_path = str(Path(__file__).parent.absolute())
    file = open(_root_path + "/config.json", "r")
    json_dict = loads(file.read())
    file.close()
    global amount_of_retrying_sending_an_answer
    amount_of_retrying_sending_an_answer = json_dict['amount_of_retrying_sending_an_answer']
    global answer_time_for_the_bot
    answer_time_for_the_bot = json_dict['answer_time_for_the_bot']
    info("api_globals initialized.")
    global test_depth
    test_depth = json_dict['test_depth']
