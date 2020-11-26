# InformatiCup 2021 - spe_ed bot
# Team:
# ███████╗████████╗ ██████╗ ██╗     ██████╗ ███████╗██████╗ ███████╗████████╗███████╗██╗███╗   ██╗███████╗
# ██╔════╝╚══██╔══╝██╔═══██╗██║     ██╔══██╗██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝██║████╗  ██║██╔════╝
# ███████╗   ██║   ██║   ██║██║     ██████╔╝█████╗  ██████╔╝███████╗   ██║   █████╗  ██║██╔██╗ ██║█████╗
# ╚════██║   ██║   ██║   ██║██║     ██╔═══╝ ██╔══╝  ██╔══██╗╚════██║   ██║   ██╔══╝  ██║██║╚██╗██║██╔══╝
# ███████║   ██║   ╚██████╔╝███████╗██║     ███████╗██║  ██║███████║   ██║   ███████╗██║██║ ╚████║███████╗
# ╚══════╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝
# programmed by Sandra Jasmine Bernich and Jonas Marvin Huhndorf

# ASCII-Art designed with: http://patorjk.com/software/taag/

from asyncio import get_event_loop

from api import apifeedback_global_variables
from api.action_play import *
from globale_functions.move_calculations import next_move_survival
from data_classes import Player
from neuronal_network import nn_global_variables

# Initialize all global-containers
nn_global_variables.init()
apifeedback_global_variables.init()

# Start contact to server
get_event_loop().run_until_complete(start_ws())

# Just for Testing:
# with open("./json_testfiles/000.json", "r") as file:
#    json_testfile = file.read()
# data_class = map_json_to_dataclass(json_testfile)

# output = next_move_survival(
#    data_class,
#    str(data_class.you),
#    "change_nothing"
# )
# print(output)
