# Python-libraries
import os
import time
import asyncio
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


# Connection and communication with the server.
async def start_ws():
    async with connect(f'{URL}?key={KEY}') as websocket:
        while True:
            play_map = await websocket.recv()
            api_globals.game_as_class = map_json_to_dataclass(play_map)

            # Just for testing. TODO("remove")
            print(api_globals.game_as_class)

            # Disconnect from server if game is over.
            if not api_globals.game_as_class.running:
                return

            start_new_thread(start_calculation, (1, ))

            # Set sleep-time before answering.
            sleep_time = (api_globals.game_as_class.deadline - datetime.utcnow()).total_seconds()
            # One second for answering.
            sleep_time -= 1

            # Just waits if the deadline is in the future.
            # It could - for example - be the case, that the server sends an old json-file.
            if sleep_time > 0:
                time.sleep(sleep_time)

            # Example of sending an answer for the server. TODO("Proper implementation")
            await websocket.send(generated_json(f'{api_globals.action}'))

            # TODO("Sleep-time must be less than deadline (find right time for answering)")
            # TODO("Implement answering after sleeping!")

            # TODO("What's about error-handling?")
