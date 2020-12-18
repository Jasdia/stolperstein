from data_classes.manual_calculation.ManuelCalculatedPlayer import ManuelCalculatedPlayer
from data_classes.manual_calculation.ManualCalculatedGame import ManualCalculatedGame
from data_classes.api.Player import Player
import api.api_feedback_global_variables as api_globals
import calculate_next_step.mc_global_variables as mc_globals


# Simplifies the data and maps Game on ManuelCalculatedGames
def simplify_game_classes():
    players: [ManuelCalculatedPlayer] = [simple_player_mapping(api_globals.game_as_class.players[str(api_globals.game_as_class.you)], api_globals.game_as_class.you)]
    for player in api_globals.game_as_class.players.items():
        simple_player = simple_player_mapping(player[1], int(player[0]))
        if player[0] != str(api_globals.game_as_class.you) and player[1].active:
            players.append(simple_player)

    new_cells = [[0]*api_globals.game_as_class.width for i in range(api_globals.game_as_class.height)]

    for column in range(0, api_globals.game_as_class.height - 1):
        for row in range(0, api_globals.game_as_class.width - 1):
            new_cells[column][row] = api_globals.game_as_class.cells[column][row]
            if api_globals.game_as_class.cells[column][row] != 0:
                new_cells[column][row] = 10
    mc_globals.simplified_game_class = ManualCalculatedGame(
        api_globals.game_as_class.width,
        api_globals.game_as_class.height,
        new_cells,
        players,
        api_globals.game_as_class.you
    )
    # print(mc_globals.simplified_game_class)


# This function maps a Player on a SimplePlayer
def simple_player_mapping(player: Player, number: int):
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
        number
    )
