# Other modules from this project
# classes:
from data_classes.manual_calculation.ManuelCalculatedPlayer import ManuelCalculatedPlayer
from data_classes.api.Player import Player
# global variables (see conventions in *_global_variables.py):
import api.api_feedback_global_variables as api_globals


# Simplifies the data and maps Game on ManuelCalculatedGames
def simplify_game_data():
    player_list = []
    for player in api_globals.game_as_class.players.items():
        if player[1].active:
            simple_player = simple_player_mapping(player[1], int(player[0]))
            if not player[0] == str(api_globals.game_as_class.you):
                player_list.append(simple_player)
            else:
                player_list.insert(0, simple_player)

    game_field = [[0]*api_globals.game_as_class.width for i in range(api_globals.game_as_class.height)]

    for column in range(0, api_globals.game_as_class.height - 1):
        for row in range(0, api_globals.game_as_class.width - 1):
            game_field[column][row] = api_globals.game_as_class.cells[column][row]
            if api_globals.game_as_class.cells[column][row] != 0:
                game_field[column][row] = 10

    return game_field, player_list


# This function maps a Player on a SimplePlayer
def simple_player_mapping(player: Player, player_id: int):
    direction: (int, int)
    if player.direction == "up":
        direction = (0, 1)
    elif player.direction == "right":
        direction = (1, 0)
    elif player.direction == "down":
        direction = (0, -1)
    else:
        direction = (-1, 0)
    return ManuelCalculatedPlayer(
        player.x,
        player.y,
        direction,
        player.speed,
        True,
        player_id
    )
