from src.base_rps import GameAction


class Agent:

    def __init__(self):
        self.state = None

    def play(self):
        if not self.state:
            return GameAction.Rock
