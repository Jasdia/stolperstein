import api.apifeedback_global_variables as api_globals
from math import fmod


def next_move_survival(
        data_class,
        player_id,
        action
):
    return next_move_survival_calculation(
        data_class.players[player_id].x,
        data_class.players[player_id].y,
        data_class.players[player_id].speed,
        data_class.players[player_id].direction,
        data_class.cells,
        data_class.width,
        data_class.height,
        action
    )


def next_move_survival_calculation(
        x_position,
        y_position,
        speed,
        direction,
        field,
        x_field_size,
        y_field_size,
        action
):
    x, y = 0, 0
    if direction == 'up':
        y = 1
    elif direction == 'down':
        y = -1
    elif direction == 'left':
        x = -1
    else:
        x = 1

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

    for n in range(1, speed):
        if api_globals.amount_of_moves != 6 or n == 1 or n == speed:
            x_location = x_position + x * n
            y_location = y_position + y * n
            if 0 < x_location < x_field_size and 0 < y_location < y_field_size:
                return False
            elif field[x_location][y_location] != 0:
                return False
    return True
