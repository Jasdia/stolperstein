# created with: https://app.quicktype.io/

from dataclasses import dataclass
from data_classes.Player import Player


@dataclass
class SimpleGame:
    width: int
    height: int
    cells: [[int]]
    players: {str: Player}
    you: Player
