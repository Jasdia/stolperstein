# Python-libraries
import os
import time
import logging
from _thread import start_new_thread
from websockets import connect
from datetime import datetime

# Other modules from this project
# functions:
from api.json_answer import generated_json
from global_functions.json_class_mapper import map_json_to_dataclass
from calculate_next_step.calculation import start_calculation
# global variables (see conventions in *_global_variables.py):
import api.api_feedback_global_variables as api_globals

# Get values from environment-variables.
URL = os.getenv('URL')
KEY = os.getenv('KEY')

# TODO("Implement amount_of_moves")


# Connection and communication with the server.
async def start_ws():
    # TODO("Why is the connection this unstable?")
    async with connect(f'{URL}?key={KEY}') as websocket:
        logging.info("Connection established.")
        while True:
            try:
                play_map = await websocket.recv()
                logging.info("Server-answer: " + play_map)
                api_globals.game_as_class = map_json_to_dataclass(play_map)
                logging.info("Mapped on the class: " + str(api_globals.game_as_class))

                # Disconnect from server if game is over.
                if not api_globals.game_as_class.running:
                    logging.info("The game is over")
                    return

                if api_globals.game_as_class.players[str(api_globals.game_as_class.you)].active:
                    logging.info("We are still alive!")
                    # TODO("Smarter implementation with self-interruption and multi-answering.")
                    start_new_thread(start_calculation, (api_globals.test_depth, api_globals.amount_of_moves, ))

                    # Set sleep-time before answering.
                    sleep_time = (api_globals.game_as_class.deadline - datetime.utcnow()).total_seconds()
                    # One second for answering.
                    sleep_time -= api_globals.answer_time_for_the_bot

                    # Just waits if the deadline is in the future.
                    # It could - for example - be the case, that the server sends an old json-file.
                    if sleep_time > 0:
                        time.sleep(sleep_time)

                    # Retrying to send the answer to the server.
                    for _ in range(api_globals.amount_of_retrying_sending_an_answer):
                        try:
                            # Example of sending an answer for the server.
                            await websocket.send(generated_json(f'{api_globals.action}'))
                            logging.info("answer sent: " + api_globals.action)

                            api_globals.reset_action()
                            api_globals.amount_of_moves += 1
                            # If message is send: break for-loop.
                            break
                        # TODO("Specify exceptions...")
                        except:
                            logging.error("sending_issues: no answer sent...")

            # TODO("Specify exceptions...")
            except:
                logging.error("connection_error: retrying...")

            # TODO("What's about error-handling (documented in api-documentation)?")
