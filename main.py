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
import global_variables as api_globals

if __name__ == '__main__':
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
    # from calculate_next_step.calculation import start_calculation, _test_all_options_1
    # from calculate_next_step.data_simplification import simplify_game_data_1
    # import api.api_feedback_global_variables as api_globals
    # import calculate_next_step.mc_global_variables as mc_globals
    # # api_globals.amount_of_moves = 10
    # # print(json_testfile)
    # from multiprocessing import Value
    # from ctypes import c_wchar_p
    # from timeit import default_timer
    # # action = Value(c_wchar_p, 'change_nothing')
    # death_count = Value('i', 0)
    # killed_count = Value('i', 0)
    # start_time = default_timer()
    # _test_all_options_1(0, death_count, killed_count, simplify_game_data_1(json_testfile), 0, True, mc_globals.move_list)
    # end_time = default_timer()
    # print(end_time - start_time)
    # print(death_count.value)
    # print(killed_count.value)
    # start_calculation(2, 10, json_testfile, action, 10)
    # api_globals.game_as_class = map_json_to_dataclass(json_testfile)
    # create_grid(api_globals.game_as_class.cells, api_globals.game_as_class.players)
    # start_calculation(1)
    # from time import sleep
    # sleep(300)
