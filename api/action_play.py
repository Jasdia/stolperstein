# Python-libraries
from os import getenv
from time import sleep
from logging import info, error, critical
from _thread import start_new_thread
from websockets import connect, exceptions
from datetime import datetime
from json import loads
from traceback import print_exc

# Other modules from this project
# functions:
from api.json_answer import generated_json
from global_functions.json_class_mapper import map_json_to_dataclass
from calculate_next_step.calculation import start_calculation
# global variables (see conventions in *_global_variables.py):
import api.api_feedback_global_variables as api_globals

# Get values from environment-variables.
URL = getenv('URL')
KEY = getenv('KEY')
api_url = f'{URL}?key={KEY}'

# TODO("Implement amount_of_moves")


# Connection and communication with the server.
async def start_ws():
    # TODO("Handle: websockets.exceptions.InvalidStatusCode: server rejected WebSocket connection: HTTP 429")
    # TODO("Why is the connection this unstable?")
    try:
        async with connect(api_url, ping_interval=None) as websocket:
            info("Connection established.")
            while True:
                try:
                    play_map = loads(await websocket.recv())
                    info("Server-answer: " + str(play_map))

                    # Disconnect from server if game is over.
                    if not play_map['running']:
                        info("The game is over")
                        return

                    if play_map['players'][str(play_map['you'])]['active']:
                        info("We are still alive!")
                        # TODO("Smarter implementation with self-interruption and multi-answering.")
                        start_new_thread(start_calculation, (api_globals.test_depth, api_globals.amount_of_moves, play_map, ))

                        # Set sleep-time before answering.
                        deadline = datetime.strptime(play_map['deadline'], '%Y-%m-%dT%H:%M:%SZ')
                        sleep_time = (deadline - datetime.utcnow()).total_seconds()
                        # One second for answering.
                        sleep_time -= api_globals.answer_time_for_the_bot

                        # Just waits if the deadline is in the future.
                        # It could - for example - be the case, that the server sends an old json-file.
                        if sleep_time > 0:
                            sleep(sleep_time)

                        # Retrying to send the answer to the server.
                        for _ in range(api_globals.amount_of_retrying_sending_an_answer):
                            try:
                                # Example of sending an answer for the server.
                                await websocket.send(generated_json(f'{api_globals.action}'))
                                info("answer sent: " + api_globals.action)

                                api_globals.reset_action()
                                api_globals.amount_of_moves += 1
                                # If message is send: break for-loop.
                                break
                            # TODO("Specify exceptions...")
                            except Exception as exc:
                                error(exc)
                                error("sending_issues: no answer sent...")

                # TODO("Specify exceptions...")
                except exceptions.ConnectionClosed as exc:
                    if exc.code == 1006:
                        error("connection lost because of error 1006. Try reconnecting")
                        websocket = await connect(api_url, ping_interval=None)
                    else:
                        critical(exc)
                        critical(print_exc())
                        critical("Connection closed on unpredicted reason.")
                        return
                except Exception as exc:
                    critical(exc)
                    critical(print_exc())
                    critical("Connection closed on unpredicted reason.")
                    return
    except exceptions.InvalidStatusCode as exc:
        error(exc.args)
        if exc.status_code == 429:
            info("try reconnecting in one minute...")
            sleep(60)
            await start_ws()
        else:
            critical(exc)
            critical(print_exc())
            critical("Unknown error accrued. The bot will exit at this point.")
            return
    except Exception as exc:
        critical(exc)
        critical(print_exc())
        critical("Unknown error accrued. The bot will exit at this point.")

    # TODO("What's about error-handling (documented in api-documentation)?")
