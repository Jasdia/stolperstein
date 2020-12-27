# Python-libraries
from math import fmod
# from _thread import start_new_thread
from multiprocessing import Process, Value
from logging import info, root, basicConfig, INFO
from deprecated import deprecated
from copy import deepcopy

# Other modules from this project
# global variables (see conventions in *_global_variables.py):
import calculate_next_step.mc_global_variables as mc_globals
# import api.api_feedback_global_variables as api_globals
# functions:
from calculate_next_step.data_simplification import simplify_game_data


# This function is called from outside to start all functions in this file.
# It maps the players and the field on our locale variables.
# Every pre-blocked field is set to 10.
# At last it starts the test_all_options-function with the default-values (for recursion)
def start_calculation(test_depth, step, play_map, action, amount_of_moves):
    # mc_globals.rest_highest_test_step()
    play_map = simplify_game_data(play_map)
    highest_test_step = Value('i', -1)
    for i in range(test_depth):
        Process(target=_move_iteration, args=(i, step, deepcopy(play_map), action, highest_test_step, amount_of_moves)).start()
        # start_new_thread(_move_iteration, (i, step, play_map, ))


def _move_iteration(test_depth, step, play_map, action, highest_test_step, amount_of_moves):
    basicConfig()
    root.setLevel(INFO)
    info("manuel_calculation started with depth " + str(test_depth))
    mc_globals._init()
    result = {}
    for move in mc_globals.move_list:
        play_map = _calculate_move(0, move, play_map, amount_of_moves)
        result[move] = _test_all_options(1, 0, 0, play_map, test_depth, move, amount_of_moves)

    next_action = mc_globals.move_list[0]
    for move in mc_globals.move_list:
        if result[move][0] < result[next_action][0]:
            next_action = move
        elif result[move][0] == result[next_action][0] and result[move][1] > result[next_action][1]:
            next_action = move

    if amount_of_moves == step and test_depth > highest_test_step.value:
        with action.get_lock():
            action.value = next_action
        with highest_test_step.get_lock():
            highest_test_step.value = test_depth
        info("manuel_calculation finished with depth " + str(test_depth))
        info(result)
        info("Answer decided to set to " + next_action)
    else:
        info("manuel_calculation with depth " + str(test_depth) + " finished too late")


# Calculates a move of one player. The position is needed to get the right filed.
# It sets the track of the move (as id on the field) and returns True or False whether the player survives.
# def _set_move(player: ManuelCalculatedPlayer, field, players):
def _calculate_move(position: int, action: str, play_map, amount_of_moves):
    x_plus_y = play_map.players[position].direction[0] + play_map.players[position].direction[1]
    if action == "turn_left":
        play_map.players[position].direction[0] = fmod((play_map.players[position].direction[0] + x_plus_y), 2)
        play_map.players[position].direction[1] = fmod((play_map.players[position].direction[1] - x_plus_y), 2)
    elif action == "turn_right":
        play_map.players[position].direction[0] = fmod((play_map.players[position].direction[0] - x_plus_y), 2)
        play_map.players[position].direction[1] = fmod((play_map.players[position].direction[1] + x_plus_y), 2)
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
        play_map.players[position].x = int(play_map.players[position].x + play_map.players[position].direction[0])
        play_map.players[position].y = int(play_map.players[position].y + play_map.players[position].direction[1])
        # Checks whether the player leaves the field.
        if not (0 <= play_map.players[position].x < play_map.width and 0 <= play_map.players[position].y < play_map.height):
            play_map.players[position].surviving = False
            return play_map
        # Checks if the player assigns the cell (because of the gap in the 6. move).
        elif fmod(amount_of_moves, 6) != 0 or n == 1 or n == play_map.players[position].speed:
            # Checks whether the cell is blocked by some player in this game.
            if play_map.cells[play_map.players[position].y][play_map.players[position].x] > 0:
                play_map.players[position].surviving = False
                # Checks whether the cell is blocked by some track from the game before.
                if not play_map.cells[play_map.players[position].y][play_map.players[position].x] == 10:
                    # Identifies player and kills him too.
                    for idx, other in enumerate(play_map.players):
                        if other.player_id == play_map.cells[play_map.players[position].y][play_map.players[position].x]:
                            if play_map.players[idx].surviving:
                                play_map.players[idx].surviving = False
                                for _ in range(play_map.players[idx].speed):
                                    if not (play_map.players[idx].x == play_map.players[position].x and play_map.players[idx].y == play_map.players[position].y):
                                        play_map.cells[play_map.players[idx].y][play_map.players[idx].x] = 0
                                        play_map.players[idx].x = int(
                                            play_map.players[idx].x - play_map.players[idx].direction[0])
                                        play_map.players[idx].y = int(
                                            play_map.players[idx].y - play_map.players[idx].direction[1])
                            else:
                                # TODO("Implement backwards-calculation")
                                print("")
                            break
                    # Sets the field on 10, because both players are dead.
                    play_map.cells[play_map.players[position].y][play_map.players[position].x] = 10
                return play_map
            # If the move is all right,sets the id on the cell.
            else:
                play_map.cells[play_map.players[position].y][play_map.players[position].x] = play_map.players[position].player_id
    # Returns True if the player survives the action.
    return play_map


# TODO("Check if it really works!")
# TODO("Check if comments are still right")
# Recursive function for testing all possible moves of all players (every single combination).
# Sets the result to mc_globals.result.
# The position ist for detecting the current player in the field and player-list.
# death_count counts how often we die at a specific action (in every single combination).
# killed_count counts how often other player die by a single action of us.
def _test_all_options(position, death_count, killed_count, play_map, test_depth, tested_move, amount_of_moves):
    # End-Statement if there is no player left at the position.
    # or if the calculation-depth is reached
    if position == len(play_map.players):
        print(tested_move + " with depth " + str(test_depth) + " at position " + str(position))
        if not test_depth == 0:
            # new_players = []
            # for idx, player in enumerate(play_map['players']):
            #     if player.surviving or idx == 0:
            #         new_players.append(player)
            # play_map['players'] = new_players
            tmp_map = deepcopy(play_map)
            for column in range(0, tmp_map.height - 1):
                for row in range(0, tmp_map.width - 1):
                    if tmp_map.cells[column][row] != 0:
                        tmp_map.cells[column][row] = 10
            death_count, killed_count = _test_all_options(0, death_count, killed_count, tmp_map, test_depth - 1,
                                                          tested_move, amount_of_moves)
        else:
            for index, player in enumerate(play_map.players):
                if not player.surviving:
                    if index == 0:
                        death_count += 1
                    else:
                        killed_count += 1
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
                # Function calls itself (recursion)
                death_count, killed_count = _test_all_options(position + 1, death_count, killed_count,
                                                              _calculate_move(position, move, deepcopy(play_map), amount_of_moves),
                                                              test_depth, tested_move, amount_of_moves)
            else:
                # Function calls itself (recursion)
                death_count, killed_count = _test_all_options(position + 1, death_count, killed_count, deepcopy(play_map),
                                                              test_depth, tested_move, amount_of_moves)

            # Sets the death_count and killed_count in result if the first player (we) is re-reached and resets the
            # values.
            # if position == 0:
            #     result = [result[0] + death_count, result[1] + killed_count]
            #     death_count, killed_count = 0, 0
            # Evaluates the combination if the last player is reached.
            # if position == len(play_map.players) - 1 and test_depth == 0:
            #     for index, player in enumerate(play_map.players):
            #         if not player.surviving:
            #             if index == 0:
            #                 death_count += 1
            #             else:
            #                 killed_count += 1
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
