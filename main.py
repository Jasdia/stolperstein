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
import logging

# Other modules from this project
# functions:
from api.action_play import start_ws
# global variables (see conventions in *_global_variables.py):
import calculate_next_step.mc_global_variables as mc_globals
import api.api_feedback_global_variables as api_globals

# Initialize all global-containers
api_globals._init()
mc_globals._init()

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)

# Start contact to server
logging.info("The bot has started...")
get_event_loop().run_until_complete(start_ws())

# ==================================================================
# Just for Testing:
# json_testfile = open("./json_test_files/000.json", "r").read()
# api_globals.game_as_class = map_json_to_dataclass(json_testfile)
# create_grid(api_globals.game_as_class.cells, api_globals.game_as_class.players)
# start_calculation(1)
