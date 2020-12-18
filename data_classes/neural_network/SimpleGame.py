# created with: https://app.quicktype.io/

from dataclasses import dataclass
from data_classes.neural_network.SimplePlayer import SimplePlayer


@dataclass
class SimpleGame:
    width: int
    height: int
    cells: [[int]]
    players: {str: SimplePlayer}
    you: SimplePlayer
