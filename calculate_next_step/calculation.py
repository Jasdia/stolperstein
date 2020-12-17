# Python-libraries
from math import fmod

# Other modules from this project
# classes:
from data_classes.ManuelCalculatedPlayer import ManuelCalculatedPlayer
# global variables (see conventions in *_global_variables.py):
import calculate_next_step.mc_global_variables as mc_globals
import api.api_feedback_global_variables as api_globals

# TODO("Remove")
# Contains the field with the moves of the players
# Third dimension is designed for keeping all fields and rollback to the last player
#test_filed: [[[int]]]

# TODO("Remove")
# Contains the list of the active players (with simplified data).
# The first Player in the list are we.
#test_players: [ManuelCalculatedPlayer]


# This function is called from outside to start all functions in this file.
# It maps the players and the field on our locale variables.
# Every pre-blocked field is set to 10.
# At last it starts the test_all_options-function with the default-values (for recursion)
def start_calculation():
    #global test_filed
    #global test_players
    #test_players = mc_globals.simplified_game_class.players
    #test_filed = [mc_globals.simplified_game_class.cells for i in range(len(test_players))]

    test_all_options(0, 0, 0, mc_globals.simplified_game_class.cells, mc_globals.simplified_game_class.players, mc_globals.test_depth)

    # This print is just for testing-purpose
    print("Action, death_count, kill_count:")
    for output in mc_globals.result.items():
        print(output[0], ", ", output[1][0], ", ", output[1][1])

    # Calculate percentage of deaths.
    for move in mc_globals.result:
        if mc_globals.result[move][0] > 0:
            mc_globals.result[move][0] = (len(mc_globals.result)**(len(mc_globals.simplified_game_class.players)-1))/mc_globals.result[move][0]

    # This print is just for testing-purpose
    print("Action, death_count, kill_count:")
    for output in mc_globals.result.items():
        print(output[0], ", ", output[1][0], ", ", output[1][1])


# Calculates a move of one player. The position is needed to get the right filed.
# It sets the track of the move (as id on the field) and returns True or False whether the player survives.
def set_move(player: ManuelCalculatedPlayer, field, players):
    #global test_filed
    #global test_players

    # Checks speed for the given limits.
    if player.speed < 1 or player.speed > 10:
        return False, field, players

    # Iterates every move of the player (cell by cell).
    for n in range(1, player.speed):
        # Checks if the player assigns the cell (because of the gap in the 6. move).
        if api_globals.amount_of_moves != 6 or n == 1 or n == player.speed:
            x_location = player.x + player.direction[0] * n
            y_location = player.y + player.direction[1] * n
            # Checks whether the player leaves the field.
            if 0 < x_location < mc_globals.simplified_game_class.width and 0 < y_location < mc_globals.simplified_game_class.height:
                return False, field, players
            # Checks whether the cell is blocked by some track from the game before.
            elif field[x_location][y_location] == 10:
                return False, field, players
            # Checks whether the cell is blocked by some player in this game.
            elif field[x_location][y_location] > 0:
                # Identifies player and kills him too.
                for idx, other in players:
                    if other.number == field[x_location][y_location]:
                        players[idx].surviving = False
                # Sets the field on 10, because both players are dead.
                field[x_location][y_location] = 10
                return False, field, players
            # If the move is all right,sets the id on the cell.
            else:
                field[x_location][y_location] += player.number
    # Returns True if the player survives the action.
    return True, field, players


# Recursive function for testing all possible moves of all players (every single combination).
# Sets the result to mc_globals.result.
# The position ist for detecting the current player in the field and player-list.
# death_count counts how often we die at a specific action (in every single combination).
# killed_count counts how often other player die by a single action of us.
def test_all_options(position, death_count, killed_count, field, players, test_depth):
    #global test_filed
    #global test_players
    # End-Statement if there is no player left at the position.
    if position == len(players):
        if not test_depth == 0:
            new_players = []
            for idx, player in enumerate(players):
                if player.surviving or idx == 0:
                    new_players.append(player)
            death_count, killed_count = test_all_options(0, death_count, killed_count, field, new_players, test_depth-1)
        return death_count, killed_count
    else:
        # Iterates every possible action for the active player/ the player at this position.
        for move in mc_globals.result.keys():
            # TODO("Remove commented block!")
            # If we re-reach the first player, his field will be reset and all players are reset.
            #if position == 0:
            #    test_filed[position] = mc_globals.simplified_game_class.cells
            #    test_players = mc_globals.simplified_game_class.players
            # At every other player, the player and every following will be reset and the players field is set to the
            # field of the player before.
            #else:
            #    test_filed[position] = test_filed[position - 1]
            #    for i in range(position, len(test_players)):
            #        test_players[i] = mc_globals.simplified_game_class.players[i]

            # Interprets the action by calling the function and changes the values of the player to the new action.
            players[position].direction, players[position].speed = interpret_move(
                players[position].direction[0],
                players[position].direction[1],
                players[position].speed,
                move
            )

            # Calls the set_move-function to set the new action and checking whether the player survives.
            players[position].surviving, field, players = set_move(players[position], field, players)

            # Function calls itself (recursion)
            death_count, killed_count = test_all_options(position + 1, death_count, killed_count, field, players, test_depth)

            # Sets the death_count and killed_count in result if the first player (we) is re-reached and resets the
            # values.
            if position == 0:
                mc_globals.result[move] = [mc_globals.result[move][0] + death_count, mc_globals.result[move][1] + killed_count]
                death_count, killed_count = 0, 0
            # Evaluates the combination if the last player is reached.
            elif position == len(mc_globals.simplified_game_class.players) - 1:
                for player in players:
                    if not player.surviving:
                        if player.number == mc_globals.simplified_game_class.you:
                            death_count += 1
                        else:
                            killed_count += 1
        # returns the current death_count and killed_count values.
        return death_count, killed_count


# Translates the action (str) to the parameters of the player (sets new speed or changes direction with the x, y tuple).
# This function doesn't change any value of the player directly, but returns the parameters.
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
