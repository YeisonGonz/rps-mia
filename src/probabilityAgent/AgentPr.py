import csv
import os
from collections import Counter

from src.base_rps import GameAction


class Agent:

    def __init__(self):
        self.DEFAULT_STATE_PATH = '../data/state.csv'
        self.state = self.load_state_by_csv()
        self.last_opponent_action = None

    def play(self):
        if not self.state:
            return GameAction.Rock

        return self.counter_action(self.get_most_likely_action())

    def parser_action(self, action):
        if action == GameAction.Rock:
            return 'ROCK'
        if action == GameAction.Paper:
            return 'PAPER'
        if action == GameAction.Scissors:
            return 'SCISSORS'
        if action == GameAction.Rock:
            return 'ROCK'
        if action == GameAction.Lizard:
            return 'LIZARD'
        if action == GameAction.Spock:
            return 'SPOCK'

    def load_state_by_csv(self):
        """
        Establece el estado segun el csv con las anteriores partidas.
        """
        directory = os.path.dirname(self.DEFAULT_STATE_PATH)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self.DEFAULT_STATE_PATH):
            with open(self.DEFAULT_STATE_PATH, 'w') as file:
                pass

        state = []

        with open(self.DEFAULT_STATE_PATH, 'r') as file:
            my_reader = csv.reader(file, delimiter=',')
            for row in my_reader:
                state.append(row)

        self.state = state
        return state

    def save_game_state(self, computer_action, user_action):
        """
        Guarda una partida, en el csv
        """

        if not os.path.exists(self.DEFAULT_STATE_PATH):
            os.makedirs(os.path.dirname(self.DEFAULT_STATE_PATH), exist_ok=True)

        winning_combinations = {
            GameAction.Rock: [GameAction.Scissors, GameAction.Lizard],
            GameAction.Paper: [GameAction.Rock, GameAction.Spock],
            GameAction.Scissors: [GameAction.Paper, GameAction.Lizard],
            GameAction.Lizard: [GameAction.Spock, GameAction.Paper],
            GameAction.Spock: [GameAction.Scissors, GameAction.Rock]
        }

        if computer_action == user_action:
            computer_status = 'DRAW'
        else:
            computer_status = 'WIN' if user_action in winning_combinations[computer_action] else 'LOSE'

        new_game_state = [self.parser_action(computer_action), self.parser_action(user_action), computer_status]
        self.state.append(new_game_state) # Actualiza el estado interno.

        with open(self.DEFAULT_STATE_PATH, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(new_game_state)

        return new_game_state

    def calculate_opponent_usage(self):
        """
        Determina el porcetaje de uso de cada eleccion del oponente.
        """
        if not self.state:
            return {}

        opponent_choices = [row[1] for row in self.state]

        choice_counts = Counter(opponent_choices)

        total_choices = sum(choice_counts.values())
        percentages = {choice: round((count / total_choices) * 100,2) for choice, count in choice_counts.items()}

        return percentages

    def get_most_likely_action(self):
        """
        Obtiene la opcion mas elegida del oponente
        """
        opponent_usage = self.calculate_opponent_usage()

        most_likely_action = max(opponent_usage, key=opponent_usage.get)
        return GameAction[most_likely_action.capitalize()]

    def counter_action(self, posible_opponent_choice):
        counters = {
            GameAction.Rock: [GameAction.Paper, GameAction.Spock],
            GameAction.Paper: [GameAction.Scissors, GameAction.Lizard],
            GameAction.Scissors: [GameAction.Rock, GameAction.Spock],
            GameAction.Lizard: [GameAction.Rock, GameAction.Scissors],
            GameAction.Spock: [GameAction.Paper, GameAction.Lizard]
        }
        return counters.get(posible_opponent_choice)[0]