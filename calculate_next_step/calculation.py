# Python-libraries
from math import fmod
from _thread import start_new_thread
from logging import info
from deprecated import deprecated

# Other modules from this project
# global variables (see conventions in *_global_variables.py):
import calculate_next_step.mc_global_variables as mc_globals
import api.api_feedback_global_variables as api_globals
# functions:
from calculate_next_step.data_simplification import simplify_game_data


# This function is called from outside to start all functions in this file.
# It maps the players and the field on our locale variables.
# Every pre-blocked field is set to 10.
# At last it starts the test_all_options-function with the default-values (for recursion)
def start_calculation(test_depth, step, play_map):
    print(play_map)
    mc_globals.rest_highest_test_step()
    play_map = simplify_game_data(play_map)
    for i in range(test_depth):
        print(i)
        start_new_thread(_move_iteration, (i, step, play_map, ))


def _move_iteration(test_depth, step, play_map):
    info("manuel_calculation started with depth " + str(test_depth))
    print("lol")
    result = {}
    for move in mc_globals.move_list:
        play_map = _set_move(0, move, play_map)
        result[move] = _test_all_options(1, 0, 0, play_map, test_depth, move)

    next_action = mc_globals.move_list[0]
    for move in mc_globals.move_list:
        if result[move][0] < result[next_action][0]:
            next_action = move
        elif result[move][0] == result[next_action][0] and result[move][1] > result[next_action][1]:
            next_action = move

    if api_globals.amount_of_moves == step and test_depth > mc_globals.highest_test_step:
        api_globals.action = next_action
        mc_globals.highest_test_step = test_depth
        info("manuel_calculation finished with depth " + str(test_depth))
        info(result)
        info("Answer decided to set to " + next_action)
    else:
        info("manuel_calculation with depth " + str(test_depth) + " finished too late")


# Calculates a move of one player. The position is needed to get the right filed.
# It sets the track of the move (as id on the field) and returns True or False whether the player survives.
# def _set_move(player: ManuelCalculatedPlayer, field, players):
def _set_move(position, action, play_map):
    x_plus_y = play_map.players[position].x + play_map.players[position].y
    if action == "turn_left":
        play_map.players[position].x = fmod((play_map.players[position].x + x_plus_y), 2)
        play_map.players[position].y = fmod((play_map.players[position].y - x_plus_y), 2)
    elif action == "turn_right":
        play_map.players[position].x = fmod((play_map.players[position].x - x_plus_y), 2)
        play_map.players[position].y = fmod((play_map.players[position].y + x_plus_y), 2)
    elif action == "slow_down":
        play_map.players[position].speed -= 1
    elif action == "speed_up":
        play_map.players[position].speed += 1

    # Checks speed for the given limits.
    if not 1 <= play_map.players[position].speed <= 10:
        play_map.players[position].surviving = False
        return play_map

    # Iterates every move of the player (cell by cell).
    for n in range(1, play_map.players[position].speed + 1):
        # Checks if the player assigns the cell (because of the gap in the 6. move).
        if fmod(api_globals.amount_of_moves, 6) != 0 or n == 1 or n == play_map.players[position].speed:
            x_location = int(play_map.players[position].x + play_map.players[position].direction[0] * n)
            y_location = int(play_map.players[position].y + play_map.players[position].direction[1] * n)
            # Checks whether the player leaves the field.
            if not (0 <= x_location < play_map.width and 0 <= y_location < play_map.height):
                play_map.players[position].surviving = False
                return play_map
            # Checks whether the cell is blocked by some player in this game.
            elif play_map.cells[x_location][y_location] > 0:
                # Checks whether the cell is blocked by some track from the game before.
                if play_map.cells[x_location][y_location] == 10:
                    play_map.players[position].surviving = False
                    return play_map
                else:
                    # Identifies player and kills him too.
                    for idx, other in enumerate(play_map.players):
                        if other.player_id == play_map.cells[x_location][y_location]:
                            play_map.players[idx].surviving = False
                            break
                    # Sets the field on 10, because both players are dead.
                    play_map.cells[x_location][y_location] = 10
                    return play_map
            # If the move is all right,sets the id on the cell.
            else:
                play_map.cells[x_location][y_location] = play_map.players[position].player_id
    # Returns True if the player survives the action.
    return play_map


# TODO("Check if it really works!")
# TODO("Check if comments are still right")
# Recursive function for testing all possible moves of all players (every single combination).
# Sets the result to mc_globals.result.
# The position ist for detecting the current player in the field and player-list.
# death_count counts how often we die at a specific action (in every single combination).
# killed_count counts how often other player die by a single action of us.
def _test_all_options(position, death_count, killed_count, play_map, test_depth, tested_move):
    # End-Statement if there is no player left at the position.
    # or if the calculation-depth is reached
    if position == len(play_map.players):
        if not test_depth == 0:
            # new_players = []
            # for idx, player in enumerate(play_map['players']):
            #     if player.surviving or idx == 0:
            #         new_players.append(player)
            # play_map['players'] = new_players
            for column in range(0, play_map.height - 1):
                for row in range(0, play_map.width - 1):
                    if play_map.cells[column][row] != 0:
                        play_map.cells[column][row] = 10
            death_count, killed_count = _test_all_options(0, death_count, killed_count, play_map, test_depth - 1, tested_move)
        return death_count, killed_count
    else:
        # Iterates every possible action for the active player/ the player at this position.
        for move in mc_globals.move_list:
            # Interprets the action by calling the function and changes the values of the player to the new action.
            # play_map.players[position].direction, play_map.players[position].speed = _interpret_move(
            #     play_map.players[position].direction[0],
            #     play_map.players[position].direction[1],
            #     play_map.players[position].speed,
            #     move
            # )

            # Calls the set_move-function to set the new action and checking whether the player survives.
            if play_map.players[position].surviving:
                play_map = _set_move(position, move, play_map)

            # Function calls itself (recursion)
            death_count, killed_count = _test_all_options(position + 1, death_count, killed_count, play_map, test_depth, tested_move)

            # Sets the death_count and killed_count in result if the first player (we) is re-reached and resets the
            # values.
            # if position == 0:
            #     result = [result[0] + death_count, result[1] + killed_count]
            #     death_count, killed_count = 0, 0
            # Evaluates the combination if the last player is reached.
            if position == len(play_map.players) - 1 and test_depth == 0:
                for index, player in enumerate(play_map.players):
                    if not player.surviving:
                        if index == 0:
                            death_count += 1
                        else:
                            killed_count += 1
        # returns the current death_count and killed_count values.
        return death_count, killed_count


# Translates the action (str) to the parameters of the player (sets new speed or changes direction with the x, y tuple).
# This function doesn't change any value of the player directly, but returns the parameters.
@deprecated(reason="Included in another function.")
def _interpret_move(x, y, speed, action):
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
