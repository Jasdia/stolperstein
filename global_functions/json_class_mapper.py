# Python-libraries
import json
from datetime import datetime
from deprecated import deprecated
# Other modules from this project
# classes:
from data_classes.api.Game import Game
from data_classes.api.Player import Player


# Maps the incoming json to the Game-class and returns the object.
@deprecated(reason="This function only steals time for no purpose.")
def map_json_to_dataclass(json_string):
    json_dict = json.loads(json_string)
    # Manuel adjustment of players, because the default-mapping would interpret it as dictionary and not as objects.
    players: {str: Player} = {}
    for player in json_dict['players'].items():
        players[player[0]] = Player(**player[1])
    # Overriding players in json_dict with the manuel-mapped data.
    json_dict['players'] = players
    # There is no deadline if the game is over.
    if json_dict['running']:
        json_dict['deadline'] = datetime.strptime(json_dict['deadline'], '%Y-%m-%dT%H:%M:%SZ')
    return Game(**json_dict)
