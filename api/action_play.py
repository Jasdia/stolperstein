import os
from websockets import connect
from api.json_answer import calculated_json, generated_json
from globale_functions.json_class_mapper import map_json_to_dataclass
import api.apifeedback_global_variables as api_globals
from neuronal_network.preparations import simplify_game_classes

URL = os.getenv('URL')
KEY = os.getenv('KEY')


async def start_ws():
    async with connect(f'{URL}?key={KEY}') as websocket:
        play_map = await websocket.recv()
        api_globals.game_as_class = map_json_to_dataclass(play_map)
        print(api_globals.game_as_class)
        simplify_game_classes()

        if api_globals.action_changed == 'true':
            await websocket.send(generated_json(f'{api_globals.action}'))
        else:
            await websocket.send(calculated_json(f'{api_globals.action}'))
