# Python-libraries
from os import getenv
from time import sleep
from logging import info, error, critical
from multiprocessing import Process, Value
from websockets import connect, exceptions
from datetime import datetime
from json import loads
from traceback import print_exc
from ctypes import c_wchar_p
# Other modules from this project
# functions:
from api.json_answer import generated_json
from calculate_next_step.calculation import start_calculation
# global variables (see conventions in *_global_variables.py):
import api.api_feedback_global_variables as api_globals

# Get values from environment-variables.
URL = getenv('URL')
KEY = getenv('KEY')
api_url = f'{URL}?key={KEY}'


# Connection and communication with the server.
async def start_ws():
    try:
        async with connect(api_url, ping_interval=None) as websocket:
            amount_of_moves = Value("i", 1)
            info("Connection established.")
            while True:
                try:
                    play_map = loads(await websocket.recv())
                    info("Server-answer: " + str(play_map))
                    action = Value(c_wchar_p, 'change_nothing')

                    # Disconnect from server if game is over.
                    if not play_map['running']:
                        info("The game is over")
                        for player in play_map['players'].values():
                            if player['active']:
                                info(player['name'] + " won the game!")
                        return

                    if play_map['players'][str(play_map['you'])]['active']:
                        info("We are still alive!")
                        # TODO("Smarter implementation with self-interruption and multi-answering.")
                        with amount_of_moves.get_lock():
                            Process(target=start_calculation, args=(api_globals.test_depth, amount_of_moves.value,
                                                                    play_map, action, amount_of_moves)).start()

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
                                with action.get_lock():
                                    await websocket.send(generated_json(f'{action.value}'))
                                    info("answer sent: " + action.value)

                                with amount_of_moves.get_lock():
                                    amount_of_moves.value += 1
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
