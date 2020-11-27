from data_classes.SimplePlayer import SimplePlayer
from data_classes.SimpleGame import SimpleGame
import neuronal_network.nn_global_variables as nn_globals
import api.api_feedback_global_variables as api_globals


# This methode maps the GameClass on the SimpleGameClass.
# This allows a simplification of the data for the neuronal network.
# Every unnecessary data will not be mapped ant the str will be translated to int.
# This specific method will also evaluate the last step by checking if the Game is over,
# if we are still living and if we killed someone.
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
                    print("TODO('if we killed him: nn_reward else: do nothing')")
        nn_globals.simplified_game_class = SimpleGame(
            api_globals.game_as_class.width,
            api_globals.game_as_class.height,
            api_globals.game_as_class.cells,
            players,
            you
        )
    else:
        if api_globals.game_as_class.players[str(api_globals.game_as_class.you)]['active']:
            print("TODO('Implementing nn_reward")
        else:
            print("TODO('Implement nn_punishment')")


# This methode maps the GameClass on the SimpleGameClass.
# This allows a simplification of the data for the neuronal network.
# Every unnecessary data will not be mapped ant the str will be translated to int.
# This specific methode does not evaluate the last step and is only called at the first action
# in a game or in the learning process with saved json-files.
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


# This function maps a Player on a SimplePlayer
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
