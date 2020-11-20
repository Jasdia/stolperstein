from api.action_play import amount_of_moves


def next_move_survival_calculation(x_position, y_position, speed, direction, field):
    x, y = 0
    if direction == 'up':
        y = 1
    elif direction == 'down':
        y = -1
    elif direction == 'left':
        x = -1
    else:
        x = 1

    for n in range(1, speed):
        if not amount_of_moves == 6 and n != 1 and n != speed:
            if field[x_position + x * n][y_position + y * n] != 0:
                return False

    return True
