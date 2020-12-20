# TODO("Remove 'created with'-comment.")
# created with: https://app.quicktype.io/

# Python-libraries
from deprecated import deprecated
from dataclasses import dataclass

# Other modules from this project
# classes:
from data_classes.neural_network.SimplePlayer import SimplePlayer


@deprecated(reason="Probably oversize!")
@dataclass
class SimpleGame:
    width: int
    height: int
    cells: [[int]]
    players: {str: SimplePlayer}
    you: SimplePlayer
