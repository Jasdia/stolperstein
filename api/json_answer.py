# Generates a json from the chosen action fo sending it to the game-server.
def generated_json(action):
    action_play = '{"action": "' + action + '"}'
    return action_play
