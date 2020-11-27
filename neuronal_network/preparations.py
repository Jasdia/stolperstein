from data_classes.SimplePlayer import SimplePlayer
from data_classes.SimpleGame import SimpleGame
import neuronal_network.nn_global_variables as nn_globals
import api.apifeedback_global_variables as api_globals


def simplify_game_classes_with_evaluation():
    if api_globals.game_as_class.players[str(api_globals.game_as_class.you)]['active']:
        players: {str: SimplePlayer} = {}
        you = None
        for player in api_globals.game_as_class.players.items():
            if player[1]["active"]:
                simple_player = simple_player_mapping(player[1])
                if player[0] == str(api_globals.game_as_class.you):
                    you = simple_player
                else:
                    players[player[0]] = simple_player
            else:
                if player[0] == api_globals.game_as_class.you:
                    print("TODO('Implement nn_punishment')")
                    return
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
        return


def simplify_game_classes_without_evaluation():
    players: {str: SimplePlayer} = {}
    you = None
    for player in api_globals.game_as_class.players.items():
        simple_player = simple_player_mapping(player[1])
        if player[0] == str(api_globals.game_as_class.you):
            you = simple_player
        elif player[1]["active"]:
            players[player[0]] = simple_player
    nn_globals.simplified_game_class = SimpleGame(
        api_globals.game_as_class.width,
        api_globals.game_as_class.height,
        api_globals.game_as_class.cells,
        players,
        you
    )


def simple_player_mapping(player: dict):
    direction: int
    if player['direction'] == "up":
        direction = 0
    elif player['direction'] == "right":
        direction = 1
    elif player['direction'] == "down":
        direction = 2
    else:
        direction = 3
    return SimplePlayer(
        player['x'],
        player['y'],
        direction,
        player['speed']
    )
