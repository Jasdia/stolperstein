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
