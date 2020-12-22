# Python-libraries
from dataclasses import dataclass

# Other modules from this project
# classes:
from data_classes.manual_calculation.ManuelCalculatedPlayer import ManuelCalculatedPlayer


@dataclass
class ManuelCalculatedGame:
    width: int
    height: int
    cells: [[int]]
    # We are the player at position 0
    players: [ManuelCalculatedPlayer]
