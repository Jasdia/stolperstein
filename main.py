from asyncio import get_event_loop
from api.action_play import *
from globale_functions.move_calculations import next_move_survival_calculation
from data_classes import Player

# get_event_loop().run_until_complete(start_ws())

with open("./json_testfiles/000.json", "r") as file:
    json_testfile = file.read()
data_class = map_json_to_dataclass(json_testfile)
# Just for finding the error:
# print(type(data_class.players.get(str(data_class.you))))
# print(data_class.players[str(data_class.you)])
# print(type(data_class.running), data_class.running)
output = next_move_survival_calculation(
    data_class.players[str(data_class.you)].x,
    data_class.players[str(data_class.you)].y,
    data_class.players[str(data_class.you)].speed,
    data_class.players[str(data_class.you)].direction,
    data_class.cells,
    data_class.width,
    data_class.height,
    "change_nothing"
)
print(output)
