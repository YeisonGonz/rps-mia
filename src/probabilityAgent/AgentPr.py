from src.base_rps import GameAction


class Agent:

    def __init__(self):
        self.DEFAULT_STATE_PATH = '../data/state.csv'
        self.state = None
        self.last_opponent_action = None

    def play(self):
        if not self.state:
            return GameAction.Rock
