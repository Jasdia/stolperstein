# created with: https://app.quicktype.io/

from dataclasses import dataclass
from datetime import datetime
from data_classes.api.Player import Player


@dataclass
class Game:
    width: int
    height: int
    cells: [[int]]
    players: {str: Player}
    you: int
    running: bool
    deadline: datetime
