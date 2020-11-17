import json
from data_classes.Game import Game


def map_json_to_dataclass(json_string):
    json_dict = json.loads(json_string)
    return Game(**json_dict)
