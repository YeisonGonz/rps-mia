import csv
import os
from src.base_rps import GameAction
from collections import Counter

class Agent:

    def __init__(self):
        self.DEFAULT_STATE_PATH = '../data/state.csv'
        self.state = self.load_state_by_csv()

    def play(self):
        if not self.state:
            return GameAction.Rock

        opponent_usage = self.calculate_opponent_usage()
        posible_opponent_choice = max(opponent_usage, key=opponent_usage.get)

        if posible_opponent_choice == 'PAPER':
            posible_opponent_choice = GameAction.Paper
        if posible_opponent_choice == 'ROCK':
            posible_opponent_choice = GameAction.Rock
        if posible_opponent_choice == 'SCISSORS':
            posible_opponent_choice = GameAction.Scissors

        return self.counter_action(posible_opponent_choice)


    def load_state_by_csv(self):
        if not os.path.exists(self.DEFAULT_STATE_PATH):
            return None

        state = []

        with open(self.DEFAULT_STATE_PATH, 'r') as file:
            my_reader = csv.reader(file, delimiter=',')
            for row in my_reader:
                state.append(row)

        self.state = state
        return state

    def save_game_state(self, computer_action, user_action, computer_status):
        if not os.path.exists(self.DEFAULT_STATE_PATH):
            os.makedirs(os.path.dirname(self.DEFAULT_STATE_PATH), exist_ok=True)

        new_game_state = [computer_action, user_action, computer_status]
        with open(self.DEFAULT_STATE_PATH, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(new_game_state)

        return new_game_state

    def calculate_opponent_usage(self):
        if not self.state:
            return {}

        opponent_choices = [row[1] for row in self.state]

        choice_counts = Counter(opponent_choices)

        total_choices = sum(choice_counts.values())
        percentages = {choice: round((count / total_choices) * 100,2) for choice, count in choice_counts.items()}

        return percentages

    def counter_action(self, posible_opponent_choice):
        counters = {
            GameAction.Rock.value: GameAction.Paper,
            GameAction.Paper.value: GameAction.Scissors,
            GameAction.Scissors.value: GameAction.Rock
        }
        return counters.get(posible_opponent_choice)