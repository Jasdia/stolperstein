# created with: https://app.quicktype.io/

from dataclasses import dataclass


@dataclass
class SimplePlayer:
    x: int
    y: int
    direction: int
    speed: int
