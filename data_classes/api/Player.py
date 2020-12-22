# TODO("Remove 'created with'-comment.")
# created with: https://app.quicktype.io/

# Python-libraries
from dataclasses import dataclass
from deprecated import deprecated


@deprecated(reason="Not useful at all.")
@dataclass
class Player:
    x: int
    y: int
    direction: str
    speed: int
    active: bool
    # Is only sent in the last json from the server (if the game is over).
    name: str = ""
