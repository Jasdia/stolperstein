import os
from websockets import connect
from api.json_answer import calculated_json, generated_json
from globale_functions.json_class_mapper import map_json_to_dataclass
from data_classes.Game import Game

URL = os.getenv('URL')
KEY = os.getenv('KEY')


async def start_ws():
    async with connect(f'{URL}?key={KEY}') as websocket:
        global game_as_class
        global amount_of_moves

        play_map = await websocket.recv()
        game_as_class = map_json_to_dataclass(play_map)
        print(game_as_class)

        if action_changed == 'true':
            await websocket.send(generated_json(f'{action}'))
        else:
            await websocket.send(calculated_json(f'{action}'))
