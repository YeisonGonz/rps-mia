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