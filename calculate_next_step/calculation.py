from math import fmod
import calculate_next_step.mc_global_variables as mc_globals
import api.api_feedback_global_variables as api_globals
from data_classes.ManuelCalculatedPlayer import ManuelCalculatedPlayer

test_filed: [[[int]]]
test_players: [ManuelCalculatedPlayer]


def start_calculation():
    global test_filed
    global test_players
    test_players = mc_globals.simplified_game_class.players
    test_filed = [mc_globals.simplified_game_class.cells for i in range(len(test_players))]
    print("Action, death_count, kill_count:")
    for output in mc_globals.result.items():
        print(output[0], ", ", output[1][0], ", ", output[1][1])
    test_all_options(0, 0, 0)


def set_move(player: ManuelCalculatedPlayer, position):
    global test_filed
    global test_players
    for n in range(1, player.speed):
        if api_globals.amount_of_moves != 6 or n == 1 or n == player.speed:
            x_location = player.x + player.direction[0] * n
            y_location = player.y + player.direction[1] * n
            if 0 < x_location < mc_globals.simplified_game_class.width and 0 < y_location < mc_globals.simplified_game_class.height:
                return False
            elif test_filed[position][x_location][y_location] == 10:
                return False
            elif test_filed[position][x_location][y_location] > 0:
                for other in test_players:
                    if other.number == test_filed[position][x_location][y_location]:
                        other.surviving = False
                test_filed[position][x_location][y_location] = 10
                return False
            else:
                test_filed[position][x_location][y_location] += player.number
    return True


def test_all_options(position, death_count, killed_count):
    global test_filed
    global test_players
    if position == len(mc_globals.simplified_game_class.players):
        return death_count, killed_count
    else:
        for move in mc_globals.result.keys():
            if position == 0:
                test_filed[position] = mc_globals.simplified_game_class.cells
                test_players = mc_globals.simplified_game_class.players
            else:
                test_filed[position] = test_filed[position - 1]
                for i in range(position, len(test_players)):
                    test_players[i] = mc_globals.simplified_game_class.players[i]

            test_players[position].direction, test_players[position].speed = \
                interpret_move(
                    test_players[position].direction[0],
                    test_players[position].direction[1],
                    test_players[position].speed,
                    move
                )

            test_players[position].surviving = set_move(test_players[position], position)

            death_count, killed_count = test_all_options(position + 1, death_count, killed_count)

            if position == 0:
                mc_globals.result[move] = [death_count, killed_count]
                death_count, killed_count = 0, 0
            elif position == len(mc_globals.simplified_game_class.players) - 1:
                for player in test_players:
                    if not player.surviving:
                        if player.number == mc_globals.simplified_game_class.you:
                            death_count += 1
                        else:
                            killed_count += 1
        return death_count, killed_count


def interpret_move(x, y, speed, action):
    x_plus_y = x + y
    if action == "turn_left":
        x = fmod((x + x_plus_y), 2)
        y = fmod((y - x_plus_y), 2)
    elif action == "turn_right":
        x = fmod((x - x_plus_y), 2)
        y = fmod((y + x_plus_y), 2)
    elif action == "slow_down":
        speed -= 1
    elif action == "speed_up":
        speed += 1
    return (x, y), speed
