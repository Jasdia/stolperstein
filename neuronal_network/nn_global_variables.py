from data_classes.SimpleGame import SimpleGame

simplified_game_class: SimpleGame
dead_players: list


def init():
    global simplified_game_class
    simplified_game_class = None
    global dead_players
    dead_players = []
