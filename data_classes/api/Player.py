# TODO("Remove 'created with'-comment.")
# created with: https://app.quicktype.io/

# Python-libraries
from dataclasses import dataclass


@dataclass
class Player:
    x: int
    y: int
    direction: str
    speed: int
    active: bool
