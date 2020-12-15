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


# Other modules from this project
# functions:
from api.action_play import *
from calculate_next_step.class_mapping import simplify_game_classes
from calculate_next_step.calculation import start_calculation
# global variables (see conventions in *_global_variables.py):
import calculate_next_step.mc_global_variables as mc_globals
import api.api_feedback_global_variables as api_globals
import neuronal_network.nn_global_variables as nn_globals

# Initialize all global-containers
nn_globals._init()
api_globals._init()
mc_globals._init()

# Start contact to server
# get_event_loop().run_until_complete(start_ws())
# get_server_time()

# ==================================================================
# Just for Testing:
with open("./json_test_files/000.json", "r") as file:
    json_testfile = file.read()
api_globals.game_as_class = map_json_to_dataclass(json_testfile)
print(api_globals.game_as_class)
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

