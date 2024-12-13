import csv
import os
from src.base_rps import GameAction
from collections import Counter

class Agent:

    def __init__(self):
        self.DEFAULT_STATE_PATH = '../data/state.csv'
        self.state = self.load_state_by_csv()
        self.last_opponent_action = None

    def play(self):
        if not self.state:
            return GameAction.Rock

        return self.counter_action(self.sum_strategies())


    def parser_action(self, action):
        if action == GameAction.Rock:
            return 'ROCK'
        if action == GameAction.Paper:
            return 'PAPER'
        if action == GameAction.Scissors:
            return 'SCISSORS'

    def load_state_by_csv(self):
        if not os.path.exists(self.DEFAULT_STATE_PATH):
            file = open(self.DEFAULT_STATE_PATH, 'x')
            file.close()
            return []

        state = []

        with open(self.DEFAULT_STATE_PATH, 'r') as file:
            my_reader = csv.reader(file, delimiter=',')
            for row in my_reader:
                state.append(row)

        self.state = state
        return state

    def save_game_state(self, computer_action, user_action):
        if not os.path.exists(self.DEFAULT_STATE_PATH):
            os.makedirs(os.path.dirname(self.DEFAULT_STATE_PATH), exist_ok=True)

        if computer_action == user_action:
            computer_status = 'DRAW'
        elif (
                (computer_action == GameAction.Rock and user_action == GameAction.Scissors) or
                (computer_action == GameAction.Paper and user_action == GameAction.Rock) or
                (computer_action == GameAction.Scissors and user_action == GameAction.Paper)
        ):
            computer_status = 'WIN'
        else:
            computer_status = 'LOSE'

        new_game_state = [self.parser_action(computer_action), self.parser_action(user_action), computer_status]
        self.state.append(new_game_state)

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

    def get_second_most_likely_action(self):
        opponent_usage = self.calculate_opponent_usage()
        sorted_usage = sorted(opponent_usage.items(), key=lambda x: x[1], reverse=True)

        if len(sorted_usage) > 1 and not all(value == sorted_usage[0][1] for _, value in sorted_usage):
            second_most_usage = sorted_usage[1][0]
            return GameAction[second_most_usage.capitalize()]
        return None

    def get_most_likely_action(self):
        opponent_usage = self.calculate_opponent_usage()
        max_value = max(opponent_usage.values())

        if all(value == max_value for value in opponent_usage.values()):
            return None

        most_likely_action = max(opponent_usage, key=opponent_usage.get)
        return GameAction[most_likely_action.capitalize()]

    def calculate_opponent_action(self):
        pattern = [GameAction.Rock, GameAction.Paper, GameAction.Scissors]

        if not self.state:
            return None

        last_game = self.state[-1]
        agent_last_action, opponent_last_action, result = last_game
        self.last_opponent_action = opponent_last_action

        if result == 'LOSE':
            return GameAction[opponent_last_action.capitalize()]
        else:
            opponent_index = pattern.index(GameAction[opponent_last_action.capitalize()])
            if opponent_index == 2:
                opponent_index == -1
            next_action = pattern[(opponent_index + 1) % len(pattern)]
            return next_action

    def sum_strategies(self):
        opponent_action_1 = self.get_most_likely_action()
        opponent_action_2 = self.calculate_opponent_action()

        if opponent_action_1 is None:
            return opponent_action_2
        if opponent_action_1 == opponent_action_2:
            return opponent_action_1
        else:
            second_most_usage = self.get_second_most_likely_action()

            if second_most_usage == opponent_action_2:
                return second_most_usage
            else:
                return opponent_action_1

    def counter_action(self, posible_opponent_choice):
        counters = {
            GameAction.Rock.value: GameAction.Paper,
            GameAction.Paper.value: GameAction.Scissors,
            GameAction.Scissors.value: GameAction.Rock
        }
        return counters.get(posible_opponent_choice)