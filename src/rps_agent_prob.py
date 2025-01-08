from enum import IntEnum, Enum


class GameAction(IntEnum):

    Rock = 0
    Paper = 1
    Scissors = 2
    Lizard = 3
    Spock = 4

class GameResult(Enum):
    Win = 'WIN'
    Lose = 'LOSE'
    Draw = 'DRAW'

def assess_game(user_action, computer_action):
    if user_action == computer_action:
        print(f"User and computer picked {user_action.name}. Draw game!")

    outcomes = {
        (GameAction.Rock, GameAction.Scissors): (GameResult.Win, "Rock smashes scissors."),
        (GameAction.Rock, GameAction.Lizard): (GameResult.Win, "Rock crushes lizard."),
        (GameAction.Paper, GameAction.Rock): (GameResult.Win, "Paper covers rock."),
        (GameAction.Paper, GameAction.Spock): (GameResult.Win, "Paper disproves Spock."),
        (GameAction.Scissors, GameAction.Paper): (GameResult.Win, "Scissors cuts paper."),
        (GameAction.Scissors, GameAction.Lizard): (GameResult.Win, "Scissors decapitates lizard."),
        (GameAction.Lizard, GameAction.Spock): (GameResult.Win, "Lizard poisons Spock."),
        (GameAction.Lizard, GameAction.Paper): (GameResult.Win, "Lizard eats paper."),
        (GameAction.Spock, GameAction.Scissors): (GameResult.Win, "Spock smashes scissors."),
        (GameAction.Spock, GameAction.Rock): (GameResult.Win, "Spock vaporizes rock."),
    }

    result, description = outcomes.get((user_action, computer_action), (GameResult.Lose, "You lost."))

    if result == GameResult.Win:
       print(f"{description} You won!")
    else:
        print(f"{description} You lost!")


def get_computer_action():
    computer_action = agent.play()
    print(f"Computer picked {computer_action}.")

    return computer_action


def get_user_action():
    # Scalable to more options (beyond rock, paper and scissors...)
    game_choices = [f"{game_action.name}[{game_action.value}]" for game_action in GameAction]
    game_choices_str = ", ".join(game_choices)
    user_selection = int(input(f"\nPick a choice ({game_choices_str}): "))
    user_action = GameAction(user_selection)

    return user_action


def play_another_round():
    another_round = input("\nAnother round? (y/n): ")
    return another_round.lower() == 'y'


def main():

    while True:
        try:
            user_action = get_user_action()
        except ValueError:
            range_str = f"[0, {len(GameAction) - 1}]"
            print(f"Invalid selection. Pick a choice in range {range_str}!")
            continue

        computer_action = get_computer_action()
        assess_game(user_action, computer_action)
        agent.save_game_state(computer_action,user_action)

        if not play_another_round():
            break


if __name__ == "__main__":
    from probabilityAgent.AgentPr import Agent
    agent = Agent()
    main()