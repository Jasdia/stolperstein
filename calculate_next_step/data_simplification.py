# Other modules from this project
# classes:
from data_classes.ManuelCalculatedPlayer import ManuelCalculatedPlayer
from data_classes.ManuelCalculatedGame import ManuelCalculatedGame


# Simplifies the data and maps Game on ManuelCalculatedGames
def simplify_game_data(play_map):
    tmp_player_list = []
    for player in play_map['players'].items():
        if player[1]['active']:
            simple_player = _simple_player_mapping(player[1], int(player[0]))
            if not player[0] == str(play_map['you']):
                tmp_player_list.append(simple_player)
            else:
                tmp_player_list.insert(0, simple_player)

    player_list = [tmp_player_list[0]]
    for i in range(1, len(tmp_player_list)):
        if not (abs(tmp_player_list[0].x - tmp_player_list[i].x) > tmp_player_list[0].speed + tmp_player_list[i].speed+2
                or abs(tmp_player_list[0].y - tmp_player_list[i].y) > tmp_player_list[0].speed + tmp_player_list[i].speed):
            player_list.append(tmp_player_list[i])

    for column in range(play_map['height']):
        for row in range(play_map['width']):
            if not play_map['cells'][column][row] == 0:
                play_map['cells'][column][row] = 10

    return ManuelCalculatedGame(play_map['width'], play_map['height'], play_map['cells'], player_list)


# This function maps a Player on a SimplePlayer
def _simple_player_mapping(player: {str: any}, player_id: int):
    direction: (int, int)
    if player['direction'] == "up":
        direction = [0, -1]
    elif player['direction'] == "right":
        direction = [1, 0]
    elif player['direction'] == "down":
        direction = [0, 1]
    else:
        direction = [-1, 0]
    return ManuelCalculatedPlayer(
        player['x'],
        player['y'],
        direction,
        player['speed'],
        True,
        player_id
    )
