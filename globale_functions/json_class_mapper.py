import json
from data_classes.Game import Game
from data_classes.Player import Player


def map_json_to_dataclass(json_string):
    json_dict = json.loads(json_string)
    players: {str: Player} = {}
    for player in json_dict['players'].items():
        new_player = Player(
            player[1]['x'],
            player[1]['y'],
            player[1]['direction'],
            player[1]['speed'],
            player[1]['active']
        )
        players[player[0]] = new_player
    return Game(
        json_dict['width'],
        json_dict['height'],
        json_dict['cells'],
        players,
        json_dict['you'],
        json_dict['running'],
        json_dict['deadline']
    )
