from data_classes.SimplePlayer import SimplePlayer
from data_classes.SimpleGame import SimpleGame
from neuronal_network.nn_global_variables import simplified_game_class, dead_players
from api.action_play import game_as_class


def simplify_game_classes():
    global simplified_game_class
    if game_as_class.players[str(game_as_class.you)]['active']:
        simplified_game_class = SimpleGame(game_as_class.width, game_as_class.height, game_as_class.cells, [], None)
        for player in game_as_class.players.items():
            if player[0] == game_as_class.you:
                simplified_game_class.you = SimplePlayer(
                    player[1]['x'],
                    player[1]['y'],
                    player[1]['direction'],
                    player[1]['speed']
                )
            else:
                simplified_game_class.players[player[0]] = SimplePlayer(
                    player[1]['x'],
                    player[1]['y'],
                    player[1]['direction'],
                    player[1]['speed']
                )
