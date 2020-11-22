from api.action_play import amount_of_moves


def next_move_survival_calculation(x_position, y_position, speed, direction, field, x_field_size, y_field_size):
    x, y = 0, 0
    if direction == 'up':
        y = 1
    elif direction == 'down':
        y = -1
    elif direction == 'left':
        x = -1
    else:
        x = 1

    for n in range(1, speed):
        if amount_of_moves != 6 or n != 1 or n != speed:
            x_location = x_position + x * n
            y_location = y_position + y * n
            if 0 < x_location < x_field_size and 0 < y_location < y_field_size:
                if field[x_location][y_location] != 0:
                    return False

    return True
