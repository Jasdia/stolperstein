# created with: https://app.quicktype.io/

from dataclasses import dataclass


@dataclass
class Player:
    x: int
    y: int
    direction: str
    speed: int
    active: bool