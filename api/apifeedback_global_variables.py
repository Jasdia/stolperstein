from data_classes.Game import Game

action_changed: bool
action: str
amount_of_moves: int
game_as_class: Game


def init():
    global action_changed
    action_changed = 'true'
    global action
    action = 'change_nothing'
    global amount_of_moves
    amount_of_moves = 0
    global game_as_class
    game_as_class = Game()
