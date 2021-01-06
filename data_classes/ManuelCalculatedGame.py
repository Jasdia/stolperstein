# Python-libraries
from dataclasses import dataclass

# Other modules from this project
# classes:
from data_classes.ManuelCalculatedPlayer import ManuelCalculatedPlayer


@dataclass
class ManuelCalculatedGame:
    width: int
    height: int
    cells: [[int]]
    # We are the player at position 0
    players: [ManuelCalculatedPlayer]

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height and self.cells == other.cells \
               and self.players == other.players
