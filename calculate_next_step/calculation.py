# Python-libraries
from math import fmod
from multiprocessing import Process, Value
from logging import info, root, basicConfig, INFO
from copy import deepcopy

# Other modules from this project
# global variables (see conventions in *_global_variables.py):
import calculate_next_step.mc_global_variables as mc_globals
# functions:
from calculate_next_step.data_simplification import simplify_game_data
# classes:
from data_classes.api.Game import Game
from data_classes.manual_calculation.ManuelCalculatedGame import ManuelCalculatedGame


# This function is called from outside to start all functions in this file.
# It maps the players and the field on our locale variables.
# Every pre-blocked field is set to 10.
# At last it starts the test_all_options-function with the default-values (for recursion)
def start_calculation(test_depth: int, step: int, play_map: Game, action: Value, amount_of_moves: Value):
    play_map = simplify_game_data(play_map)
    highest_test_step = Value('i', -1)
    for i in range(test_depth):
        Process(target=_move_iteration,
                args=(i, step, deepcopy(play_map), action, highest_test_step, amount_of_moves)).start()


def _move_iteration(test_depth: int, step: int, play_map: ManuelCalculatedGame, action: Value, highest_test_step: Value,
                    amount_of_moves: Value):
    basicConfig()
    root.setLevel(INFO)
    info("manuel_calculation started with depth " + str(test_depth))
    mc_globals._init()
    processes = []
    with amount_of_moves.get_lock():
        is_not_6th_step = not amount_of_moves.value % 6 == 0
    result = {}
    for move in mc_globals.move_list:
        tmp_map = deepcopy(play_map)
        tmp_map = _calculate_move(0, move, tmp_map, is_not_6th_step)
        death_count = Value("i", 0)
        kill_count = Value("i", 0)
        p = Process(target=_test_all_options,
                    args=(1, death_count, kill_count, tmp_map, test_depth, is_not_6th_step, mc_globals.move_list))
        processes.append(p)
        p.start()
        result[move] = [death_count, kill_count]

    for process in processes:
        process.join()

    next_action = mc_globals.move_list[0]
    for move in mc_globals.move_list:
        with result[move][0].get_lock() and result[move][1].get_lock():
            if result[move][0].value < result[next_action][0].value:
                next_action = move
            elif result[move][0].value == result[next_action][0] and result[move][1].value > result[next_action][1].value:
                next_action = move
    with amount_of_moves.get_lock():
        if amount_of_moves.value == step and test_depth > highest_test_step.value:
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
# def _calculate_move(player: ManuelCalculatedPlayer, field, players):
def _calculate_move(position: int, action: str, play_map: ManuelCalculatedGame, is_not_6th_step: bool):
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
        elif is_not_6th_step or n == 1 or n == play_map.players[position].speed:
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
def _test_all_options(position: int, death_count: Value, kill_count: Value, play_map: ManuelCalculatedGame,
                      test_depth: int, is_not_6th_step: bool, move_list: []):
    processes = []

    # Iterates every possible action for the active player/ the player at this position.
    for move in move_list:

        if position == len(play_map.players) - 1:
            if not test_depth == 0:
                tmp_map = deepcopy(play_map)
                for column in range(tmp_map.height):
                    for row in range(tmp_map.width):
                        if tmp_map.cells[column][row] != 0:
                            tmp_map.cells[column][row] = 10
                _test_all_options(0, death_count, kill_count, tmp_map, test_depth - 1, is_not_6th_step, move_list)
            else:
                for index, player in enumerate(play_map.players):
                    if not player.surviving:
                        if index == 0:
                            with death_count.get_lock():
                                death_count.value += 1
                        else:
                            with kill_count.get_lock():
                                kill_count.value += 1
        else:
            # Calls the set_move-function to set the new action and checking whether the player survives.
            if play_map.players[position].surviving:
                # Function calls itself (recursion)
                p = Process(target=_test_all_options, args=(position + 1, death_count, kill_count,
                                                            _calculate_move(position, move, deepcopy(play_map),
                                                                            is_not_6th_step), test_depth,
                                                            is_not_6th_step, move_list))
                processes.append(p)
                p.start()
            else:
                # Function calls itself (recursion)
                p = Process(target=_test_all_options, args=(position + 1, death_count, kill_count, deepcopy(play_map),
                                                            test_depth, is_not_6th_step, move_list))
                processes.append(p)
                p.start()

    for process in processes:
        process.join()
