from src.base_rps import GameAction
from src.modelAgent.Agent import Agent


testing_agent = Agent()

def test_empty_histoy():
    """
    Comprueba que la respuesta del Agente cuando no tiene informacion en el historico de partidas
    """
    assert testing_agent.play() == GameAction.Rock