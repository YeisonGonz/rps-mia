import csv
import os
from src.base_rps import GameAction


class Agent:

    def __init__(self):
        self.DEFAULT_STATE_PATH = '../data/state.csv'
        self.state = self.load_state_by_csv()

    def play(self):
        if not self.state:
            return GameAction.Rock


    def load_state_by_csv(self):
        if not os.path.exists(self.DEFAULT_STATE_PATH):
            return None

        state = []

        with open(self.DEFAULT_STATE_PATH, 'r') as file:
            my_reader = csv.reader(file, delimiter=',')
            for row in my_reader:
                state.append(row)

        return state