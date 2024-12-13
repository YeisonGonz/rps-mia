from src.base_rps import GameAction
from src.modelAgent.Agent import Agent


testing_agent = Agent()

def test_empty_histoy():
    """
    Comprueba que la respuesta del Agente cuando no tiene informacion en el historico de partidas
    """
    assert testing_agent.play() == GameAction.Rock

def test_load_state():
    """
    Leer bien el csv del historico de partidas
    """
    testing_agent.DEFAULT_STATE_PATH = '../src/data/default_state.csv' # Pequeno csv para hacer pruebas
    assert testing_agent.load_state_by_csv() == [['ROCK','PAPER','WIN']]

def test_save_state():
    testing_agent.state = [['ROCK', 'PAPER', 'WIN']]
    testing_agent.DEFAULT_STATE_PATH = '../src/data/default_state_test.csv'
    assert testing_agent.save_game_state(GameAction.Paper,GameAction.Scissors) == ['PAPER','SCISSORS','LOSE']

def test_opponent_usage():
    testing_agent.state = [['ROCK', 'PAPER', 'WIN']]
    assert testing_agent.calculate_opponent_usage() == {'PAPER':100.0}

    testing_agent.state = [['ROCK', 'PAPER', 'WIN'],['ROCK', 'ROCK', 'DRAW']]
    assert testing_agent.calculate_opponent_usage() == {'ROCK': 50.0, 'PAPER': 50.0}

    testing_agent.state = [['ROCK', 'PAPER', 'WIN'], ['ROCK', 'ROCK', 'DRAW'],['ROCK', 'ROCK', 'DRAW']]
    assert testing_agent.calculate_opponent_usage() == {'ROCK': 66.67, 'PAPER': 33.33}

    testing_agent.state = [['ROCK', 'PAPER', 'WIN'], ['ROCK', 'ROCK', 'DRAW'], ['ROCK', 'SCISSORS', 'WIN']]
    assert testing_agent.calculate_opponent_usage() == { 'ROCK': 33.33, 'PAPER': 33.33,'SCISSORS': 33.33}

def test_counter_action():
    """
    posible_opponent_choice es el resultado de mayor porcentace que devuelve la funcion calculate_opponent_usage(),
    se basa en responder con la accion contraria a la accion mas probable del oponente.
    """

    assert testing_agent.counter_action(posible_opponent_choice=GameAction.Rock) == GameAction.Paper
    assert testing_agent.counter_action(posible_opponent_choice=GameAction.Paper) == GameAction.Scissors
    assert testing_agent.counter_action(posible_opponent_choice=GameAction.Scissors) == GameAction.Rock

def test_calculate_opponent_action_probabilities():
    """
    Esta funcion opera basandose en la segunda estartegia basada en el orden, Piedra -> Papel -> Tijera.
    """
    testing_agent.last_opponent_action = GameAction.Rock
    testing_agent.state = [['ROCK', 'ROCK', 'DRAW']]
    assert testing_agent.calculate_opponent_action() == GameAction.Paper # Siguiendo la estrategia basada en el orden, Piedra -> Papel -> Tijera

    testing_agent.last_opponent_action = GameAction.Paper
    testing_agent.state = [['ROCK', 'ROCK', 'DRAW'],['ROCK', 'PAPER', 'LOSE']] # El oponente gana y tendera a repetir la jugada
    assert testing_agent.calculate_opponent_action() == GameAction.Paper

    testing_agent.last_opponent_action = GameAction.Paper
    testing_agent.state = [['ROCK', 'ROCK', 'DRAW'],['SCISSORS', 'PAPER', 'WIN']]  # El oponente pierde, cambiando de eleccion siguiendo la estrategia
    assert testing_agent.calculate_opponent_action() == GameAction.Scissors


def test_sum_startegies():
    testing_agent.last_opponent_action = GameAction.Paper
    testing_agent.state = [['PAPER', 'PAPER', 'DRAW'],['ROCK', 'SCISSORS', 'WIN'], ['SCISSORS', 'PAPER', 'WIN']]
    assert testing_agent.sum_strategies() == GameAction.Scissors

    testing_agent.last_opponent_action = GameAction.Paper
    testing_agent.state = [['PAPER', 'ROCK', 'WIN'], ['SCISSORS', 'PAPER', 'WIN'], ['PAPER', 'SCISSORS', 'LOSE']]
    assert testing_agent.sum_strategies() == GameAction.Scissors

def test_most_likely_action():
    testing_agent.state = [['PAPER', 'PAPER', 'DRAW'], ['ROCK', 'SCISSORS', 'WIN'], ['SCISSORS', 'SCISSORS', 'DRAW']]
    assert testing_agent.get_most_likely_action() == GameAction.Scissors

    testing_agent.state = [['PAPER', 'PAPER', 'DRAW'], ['ROCK', 'PAPER', 'LOSE'], ['SCISSORS', 'SCISSORS', 'DRAW']]
    assert testing_agent.get_most_likely_action() == GameAction.Paper

    testing_agent.state = [['PAPER', 'PAPER', 'DRAW'], ['ROCK', 'ROCK', 'DRAW'], ['SCISSORS', 'ROCK', 'LOSE']]
    assert testing_agent.get_most_likely_action() == GameAction.Rock

    testing_agent.state = [['PAPER', 'PAPER', 'DRAW'], ['ROCK', 'SCISSORS', 'WIN'], ['SCISSORS', 'ROCK', 'LOSE']]
    assert testing_agent.get_most_likely_action() is None

def test_second_most_likely_action():
    testing_agent.state = [['PAPER', 'PAPER', 'DRAW'], ['ROCK', 'SCISSORS', 'WIN'], ['SCISSORS', 'SCISSORS', 'DRAW']]
    assert testing_agent.get_second_most_likely_action() == GameAction.Paper

    testing_agent.state = [['PAPER', 'PAPER', 'DRAW'], ['ROCK', 'PAPER', 'LOSE'], ['SCISSORS', 'SCISSORS', 'DRAW']]
    assert testing_agent.get_second_most_likely_action() == GameAction.Scissors

    testing_agent.state = [['PAPER', 'PAPER', 'DRAW'], ['ROCK', 'PAPER', 'LOSE'], ['SCISSORS', 'ROCK', 'LOSE']]
    assert testing_agent.get_second_most_likely_action() == GameAction.Rock

    testing_agent.state = [['PAPER', 'PAPER', 'DRAW'], ['ROCK', 'SCISSORS', 'WIN'], ['SCISSORS', 'ROCK', 'LOSE']]
    assert testing_agent.get_second_most_likely_action() is None