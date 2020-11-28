# created with: https://app.quicktype.io/

from dataclasses import dataclass


@dataclass
class ManuelCalculatedPlayer:
    x: int
    y: int
    direction: (int, int)
    speed: int
    surviving: bool
    number: int
