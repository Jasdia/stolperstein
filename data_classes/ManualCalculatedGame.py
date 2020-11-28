from dataclasses import dataclass
from data_classes.ManuelCalculatedPlayer import ManuelCalculatedPlayer


@dataclass
class ManualCalculatedGame:
    width: int
    height: int
    cells: [[int]]
    players: [ManuelCalculatedPlayer]
    you: int
