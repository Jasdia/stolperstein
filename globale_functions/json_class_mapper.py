import json
from data_classes.api.Game import Game
from data_classes.api.Player import Player


# Maps the incoming json to the Game-class and returns the object.
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
    json_dict['players'] = players
    return Game(**json_dict)
