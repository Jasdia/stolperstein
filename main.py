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
import calculate_next_step.mc_global_variables as mc_globals
from api import api_feedback_global_variables
from api.action_play import *
from globale_functions.move_calculations import next_move_survival
from data_classes import Player
from api.time_server import get_server_time
from neuronal_network import nn_global_variables
from neuronal_network.preparations import simplify_game_classes_with_evaluation, simplify_game_classes_without_evaluation
from calculate_next_step.class_mapping import simplify_game_classes
from calculate_next_step.calculation import start_calculation
from datetime import datetime

# Initialize all global-containers
nn_global_variables.init()
api_feedback_global_variables.init()
mc_globals.init()

# Start contact to server
# get_event_loop().run_until_complete(start_ws())
# get_server_time()

# ==================================================================
# Just for Testing:
with open("./json_test_files/001.json", "r") as file:
    json_testfile = file.read()
api_globals.game_as_class = map_json_to_dataclass(json_testfile)
# print(api_globals.game_as_class)
simplify_game_classes()
start_calculation()

# simplify_game_classes_with_evaluation()
# print("Qapla'!")
# simplify_game_classes_without_evaluation()
# output = next_move_survival(
#    data_class,
#    str(data_class.you),
#    "change_nothing"
# )
# print(output)

