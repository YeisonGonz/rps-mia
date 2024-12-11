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
    testing_agent.DEFAULT_STATE_PATH = '../src/data/default_state_test.csv'
    assert testing_agent.save_game_state('PAPER','SCISSORS','LOSE') == ['PAPER','SCISSORS','LOSE']

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