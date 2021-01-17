# Python-libraries
from dataclasses import dataclass


@dataclass
class ManuelCalculatedPlayer:
    x: int
    y: int
    direction: [int, int]
    speed: int
    surviving: bool
    player_id: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.direction == other.direction \
               and self.speed == other.speed and self.surviving == other.surviving and self.player_id == other.player_id
