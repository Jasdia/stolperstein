# InformatiCup 2021 - spe_ed bot
# Team:
# ███████╗████████╗ ██████╗ ██╗     ██████╗ ███████╗██████╗ ███████╗████████╗███████╗██╗███╗   ██╗
# ██╔════╝╚══██╔══╝██╔═══██╗██║     ██╔══██╗██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝██║████╗  ██║
# ███████╗   ██║   ██║   ██║██║     ██████╔╝█████╗  ██████╔╝███████╗   ██║   █████╗  ██║██╔██╗ ██║
# ╚════██║   ██║   ██║   ██║██║     ██╔═══╝ ██╔══╝  ██╔══██╗╚════██║   ██║   ██╔══╝  ██║██║╚██╗██║
# ███████║   ██║   ╚██████╔╝███████╗██║     ███████╗██║  ██║███████║   ██║   ███████╗██║██║ ╚████║
# ╚══════╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝╚═╝  ╚═══╝
# programmed by Sandra Jasmine Bernich and Jonas Marvin Huhndorf

# ASCII-Art designed with: http://patorjk.com/software/taag/


# Python-libraries
from asyncio import get_event_loop
from logging import info, INFO, basicConfig, root
from os import getenv
from websockets import connect

# Other modules from this project
# functions:
from api.action_play import start_ws
import global_variables as internal_globals

# This function starts the bot.
if __name__ == '__main__':
    # Initialize all global-containers
    internal_globals._init()

    # Sets the logging-level to INFO.
    basicConfig()
    root.setLevel(INFO)

    # Get values from environment-variables and builds up the connection.
    api_url = "{}?key={}".format(getenv('URL'), getenv('KEY'))
    server = connect(api_url, ping_interval=None)

    # Start communication with the server
    info("The bot has started...")
    get_event_loop().run_until_complete(start_ws(server))
