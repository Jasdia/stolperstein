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


# Python-libraries
from asyncio import get_event_loop
from logging import info, INFO, basicConfig, root

# Other modules from this project
# functions:
from api.action_play import start_ws
# global variables (see conventions in *_global_variables.py):
import calculate_next_step.mc_global_variables as mc_globals
import api.api_feedback_global_variables as api_globals

# Initialize all global-containers
api_globals._init()
mc_globals._init()

# Sets the logging-level to INFO.
basicConfig()
root.setLevel(INFO)

# Start contact to server
info("The bot has started...")
get_event_loop().run_until_complete(start_ws())

# ==================================================================
# Just for Testing:
# from json import loads
# json_testfile = loads(open("./json_test_files/002.json", "r").read())
# from calculate_next_step.calculation import start_calculation
# import api.api_feedback_global_variables as api_globals
# api_globals.amount_of_moves = 10
# print(json_testfile)
# start_calculation(2, 10, json_testfile)
# api_globals.game_as_class = map_json_to_dataclass(json_testfile)
# create_grid(api_globals.game_as_class.cells, api_globals.game_as_class.players)
# start_calculation(1)
# from time import sleep
# sleep(60)
