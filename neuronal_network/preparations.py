from data_classes.SimplePlayer import SimplePlayer
from data_classes.SimpleGame import SimpleGame
import neuronal_network.nn_global_variables as nn_globals
import api.apifeedback_global_variables as api_globals


def simplify_game_classes():
    print(api_globals.game_as_class)
    if api_globals.game_as_class.players[str(api_globals.game_as_class.you)]['active']:
        players: {int: SimplePlayer} = {}
        you = None
        for player in api_globals.game_as_class.players.items():
            if player[1]["active"]:
                direction: int
                if player[1]['direction'] == "up":
                    direction = 0
                elif player[1]['direction'] == "right":
                    direction = 1
                elif player[1]['direction'] == "down":
                    direction = 2
                else:
                    direction = 3
                simple_player = SimplePlayer(
                    player[1]['x'],
                    player[1]['y'],
                    direction,
                    player[1]['speed']
                )
                if player[0] == str(api_globals.game_as_class.you):
                    you = simple_player
                else:
                    players[player[0]] = simple_player
            else:
                if player[0] == api_globals.game_as_class.you:
                    print("TODO('Implement nn_punishment')")
                else:
                    print("TODO('reaction')")
        nn_globals.simplified_game_class = SimpleGame(
            api_globals.game_as_class.width,
            api_globals.game_as_class.height,
            api_globals.game_as_class.cells,
            players,
            you
        )
    else:
        print("TODO('Implement nn_punishment')")
    print(nn_globals.simplified_game_class)
