# Python-libraries
from math import fmod
import _thread
import logging

# Other modules from this project
# classes:
from data_classes.manual_calculation.ManuelCalculatedPlayer import ManuelCalculatedPlayer
# global variables (see conventions in *_global_variables.py):
import calculate_next_step.mc_global_variables as mc_globals
import api.api_feedback_global_variables as api_globals
# functions:
from calculate_next_step.data_simplification import simplify_game_data


# This function is called from outside to start all functions in this file.
# It maps the players and the field on our locale variables.
# Every pre-blocked field is set to 10.
# At last it starts the test_all_options-function with the default-values (for recursion)
def start_calculation(test_depth, step):
    mc_globals.rest_highest_test_step()
    for _ in range(test_depth):
        _thread.start_new_thread(_move_iteration, (test_depth, step, ))


# Calculates a move of one player. The position is needed to get the right filed.
# It sets the track of the move (as id on the field) and returns True or False whether the player survives.
def _set_move(player: ManuelCalculatedPlayer, field, players):
    # Checks speed for the given limits.
    if player.speed < 1 or player.speed > 10:
        return False, field, players

    # Iterates every move of the player (cell by cell).
    for n in range(1, player.speed):
        # Checks if the player assigns the cell (because of the gap in the 6. move).
        if fmod(api_globals.amount_of_moves, 6) != 0 or n == 1 or n == player.speed:
            x_location = player.x + player.direction[0] * n
            y_location = player.y + player.direction[1] * n
            # Checks whether the player leaves the field.
            if 0 < x_location < api_globals.game_as_class.width and 0 < y_location < api_globals.game_as_class.height:
                return False, field, players
            # Checks whether the cell is blocked by some track from the game before.
            elif field[x_location][y_location] == 10:
                return False, field, players
            # Checks whether the cell is blocked by some player in this game.
            elif field[x_location][y_location] > 0:
                # Identifies player and kills him too.
                for idx, other in players:
                    if other.player_id == field[x_location][y_location]:
                        players[idx].surviving = False
                # Sets the field on 10, because both players are dead.
                field[x_location][y_location] = 10
                return False, field, players
            # If the move is all right,sets the id on the cell.
            else:
                field[x_location][y_location] += player.player_id
    # Returns True if the player survives the action.
    return True, field, players


def _move_iteration(test_depth, step):
    logging.info("manuel_calculation started with depth " + test_depth)
    game_field, player_list = simplify_game_data()

    result = {}
    for move in mc_globals.move_list:
        _, _, result[move] = _test_all_options(0, 0, 0, game_field, player_list, test_depth, move, [0, 0])

    next_action = mc_globals.move_list[0]
    for move in mc_globals.move_list:
        if result[move][0] < result[next_action][0]:
            next_action = move
        elif result[move][0] == result[next_action][0] and result[move][1] > result[next_action][1]:
            next_action = move

    if api_globals.amount_of_moves == step and test_depth < mc_globals.highest_test_step:
        logging.info("manuel_calculation finished with depth " + str(test_depth))
        logging.info(result)
        logging.info("Answer decided to set to " + next_action)
        api_globals.action = next_action
        mc_globals.highest_test_step = test_depth


# TODO("Check if it really works!")
# TODO("Check if comments are still right")
# Recursive function for testing all possible moves of all players (every single combination).
# Sets the result to mc_globals.result.
# The position ist for detecting the current player in the field and player-list.
# death_count counts how often we die at a specific action (in every single combination).
# killed_count counts how often other player die by a single action of us.
def _test_all_options(position, death_count, killed_count, field, players, test_depth, tested_move, result):
    # End-Statement if there is no player left at the position.
    # or if the calculation-depth is reached
    if position == len(players):
        if not test_depth == 0:
            new_players = []
            for idx, player in enumerate(players):
                if player.surviving or idx == 0:
                    new_players.append(player)
            death_count, killed_count, result = _test_all_options(0, death_count, killed_count, field, new_players, test_depth - 1, tested_move, result)
        return death_count, killed_count, result
    else:
        # Iterates every possible action for the active player/ the player at this position.
        for idx, move in enumerate(mc_globals.move_list):
            # Interprets the action by calling the function and changes the values of the player to the new action.
            players[position].direction, players[position].speed = _interpret_move(
                players[position].direction[0],
                players[position].direction[1],
                players[position].speed,
                move
            )

            # Calls the set_move-function to set the new action and checking whether the player survives.
            players[position].surviving, field, players = _set_move(players[position], field, players)

            # Function calls itself (recursion)
            death_count, killed_count, result = _test_all_options(position + 1, death_count, killed_count, field, players, test_depth, tested_move, result)

            # Sets the death_count and killed_count in result if the first player (we) is re-reached and resets the
            # values.
            if position == 0:
                # TODO("get result as a locale variable for calling this function async many times and get death_count
                #  as percentage")
                result = [result[0] + death_count, result[1] + killed_count]
                death_count, killed_count = 0, 0
            # Evaluates the combination if the last player is reached.
            elif position == len(players) - 1:
                for index, player in enumerate(players):
                    if not player.surviving:
                        if index == 0:
                            death_count += 1
                        else:
                            killed_count += 1
        # returns the current death_count and killed_count values.
        return death_count, killed_count, result


# Translates the action (str) to the parameters of the player (sets new speed or changes direction with the x, y tuple).
# This function doesn't change any value of the player directly, but returns the parameters.
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
