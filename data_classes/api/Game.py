# TODO("Remove 'created with'-comment.")
# created with: https://app.quicktype.io/

# Python-libraries
from dataclasses import dataclass
from datetime import datetime

# Other modules from this project
# classes:
from data_classes.api.Player import Player


@dataclass
class Game:
    width: int
    height: int
    cells: [[int]]
    players: {str: Player}
    you: int
    running: bool
    # Default value for the last json (if game-over there is no deadline).
    deadline: datetime = ""
