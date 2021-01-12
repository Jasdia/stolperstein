# Python-libraries
from os import getenv
from time import sleep
from logging import info, error, critical
from multiprocessing import Process, Value
from websockets import connect, exceptions
from datetime import datetime
from json import loads
from traceback import print_exc
from ctypes import c_int
# Other modules from this project
# functions:
from api.json_answer import generated_json
from calculate_next_step.simple_calculation import move_iteration
# global variables:
import global_variables as internal_globals


# Connection and communication with the server.
async def start_ws():
    # Get values from environment-variables.
    api_url = "{}?key={}".format(getenv('URL'), getenv('KEY'))

    try:
        async with connect(api_url, ping_interval=None) as websocket:
            amount_of_moves = Value("i", 1)
            info("Connection established.")
            while True:
                try:
                    play_map = loads(await websocket.recv())
                    info("Server-answer: " + str(play_map))
                    action = Value(c_int, 0)

                    # Disconnect from server if game is over.
                    if not play_map['running']:
                        info("The game is over")
                        for player in play_map['players'].values():
                            if player['active']:
                                info(player['name'] + " won the game!")
                        return

                    if play_map['players'][str(play_map['you'])]['active']:
                        info("We are still alive!")
                        with amount_of_moves.get_lock() and action.get_lock():
                            Process(target=move_iteration, args=(amount_of_moves.value, play_map, action,
                                                                 amount_of_moves, internal_globals.move_list)).start()

                        # Set sleep-time before answering.
                        deadline = datetime.strptime(play_map['deadline'], '%Y-%m-%dT%H:%M:%SZ')
                        sleep_time = (deadline - datetime.utcnow()).total_seconds()
                        # One second for answering.
                        sleep_time -= internal_globals.answer_time_for_the_bot

                        # Just waits if the deadline is in the future.
                        # It could - for example - be the case, that the server sends an old json-file.
                        if sleep_time > 0:
                            sleep(sleep_time)

                        # Retrying to send the answer to the server.
                        for _ in range(internal_globals.amount_of_retrying_sending_an_answer):
                            try:
                                # Example of sending an answer for the server.
                                with action.get_lock():
                                    await websocket.send(generated_json(f'{internal_globals.move_list[action.value]}'))
                                    info("answer sent: " + internal_globals.move_list[action.value])

                                with amount_of_moves.get_lock():
                                    amount_of_moves.value += 1
                                # If message is send: break for-loop.
                                break
                            # TODO("Specify exceptions...")
                            except Exception as exc:
                                error("sending_issues: no answer sent...")
                    else:
                        # Set sleep-time before answering.
                        deadline = datetime.strptime(play_map['deadline'], '%Y-%m-%dT%H:%M:%SZ')
                        sleep_time = (deadline - datetime.utcnow()).total_seconds()

                        # Just waits if the deadline is in the future.
                        # It could - for example - be the case, that the server sends an old json-file.
                        if sleep_time > 0:
                            sleep(sleep_time)

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
