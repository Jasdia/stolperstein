from dataclasses import dataclass
from data_classes.manual_calculation.ManuelCalculatedPlayer import ManuelCalculatedPlayer


@dataclass
class ManualCalculatedGame:
    width: int
    height: int
    cells: [[int]]
    players: [ManuelCalculatedPlayer]
    you: int
