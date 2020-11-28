import os
import time
from websockets import connect
from datetime import datetime, timedelta
from api.json_answer import calculated_json, generated_json
from globale_functions.json_class_mapper import map_json_to_dataclass
from api.time_server import get_server_time
import api.api_feedback_global_variables as api_globals
from neuronal_network.preparations import simplify_game_classes_with_evaluation, simplify_game_classes_without_evaluation

URL = os.getenv('URL')
KEY = os.getenv('KEY')


async def start_ws():
    async with connect(f'{URL}?key={KEY}') as websocket:
        while True:
            play_map = await websocket.recv()
            api_globals.game_as_class = map_json_to_dataclass(play_map)
            print(api_globals.game_as_class)

            if not api_globals.game_as_class.running:
                return

            # simplify_game_classes_with_evaluation()
            # simplify_game_classes_without_evaluation()

            if api_globals.action_changed == 'true':
                await websocket.send(generated_json(f'{api_globals.action}'))
            else:
                await websocket.send(calculated_json(f'{api_globals.action}'))

            sleep_time = (api_globals.game_as_class.deadline-datetime.utcnow()).total_seconds()

            # Just waits if the deadline is in the future.
            # It could - for example - be the case, that the server sends an old json-file.
            if sleep_time > 0:
                time.sleep(sleep_time)


