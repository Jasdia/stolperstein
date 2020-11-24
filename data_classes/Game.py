# created with: https://app.quicktype.io/

from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime
from data_classes.Player import Player


@dataclass
class Game:
    width: int
    height: int
    cells: List[List[int]]
    players: Dict[str, Player]
    you: int
    running: bool
    deadline: datetime

    def __init__(self):
        self.players = {}  # Initialize empty dict
        for json_player in json_mapped_stuff_thingy:  # Fill with data from json
            self.players[json_player.id] = Player(json_player.x, json_player.y,....)  # Assign values to a non existent key


# bücherei = {0: book(title="Harry Potter - The Phil.."),
#             1: book(...)
#             }
#
# print(bücherei[0].title)