# TODO("Remove 'created with'-comment.")
# created with: https://app.quicktype.io/

# Python-libraries
from deprecated import deprecated
from dataclasses import dataclass


@deprecated(reason="Probably oversize!")
@dataclass
class SimplePlayer:
    x: int
    y: int
    direction: int
    speed: int
