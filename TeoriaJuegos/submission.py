from util import manhattanDistance
from game import Directions
import random
import util
from typing import Any, DefaultDict, List, Set, Tuple

from game import Agent
from pacman import GameState



class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def __init__(self):
        self.lastPositions = []
        self.dc = None

    def getAction(self, gameState: GameState):
        """
        getAction chooses among the best options according to the evaluation function.

        getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East}
        ------------------------------------------------------------------------------
        Description of GameState and helper functions:

        A GameState specifies the full game state, including the food, capsules,
        agent configurations and score changes. In this function, the |gameState| argument
        is an object of GameState class. Following are a few of the helper methods that you
        can use to query a GameState object to gather information about the present state
        of Pac-Man, the ghosts and the maze.

        gameState.getLegalActions(agentIndex):
            Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

        gameState.generateSuccessor(agentIndex, action):
            Returns the successor state after the specified agent takes the action.
            Pac-Man is always agent 0.

        gameState.getPacmanState():
            Returns an AgentState object for pacman (in game.py)
            state.configuration.pos gives the current position
            state.direction gives the travel vector

        gameState.getGhostStates():
            Returns list of AgentState objects for the ghosts

        gameState.getNumAgents():
            Returns the total number of agents in the game

        gameState.getScore():
            Returns the score corresponding to the current state of the game


        The GameState class is defined in pacman.py and you might want to look into that for
        other helper methods, though you don't need to.
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)


        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action: str) -> float:
        """
        The evaluation function takes in the current GameState (defined in pacman.py)
        and a proposed action and returns a rough estimate of the resulting successor
        GameState's value.

        The code below extracts some useful information from the state, like the
        remaining food (oldFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState: GameState) -> float:

    return currentGameState.getScore()



class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)




class MinimaxAgent(MultiAgentSearchAgent):
    """
        Agente que utiliza el algoritmo Minimax para tomar decisiones.

        Se utiliza el algoritmo Minimax para determinar el mejor movimiento posible considerando las acciones de los agentes que son el Pacman y el fantasma.
    """
    def getAction(self, estadoJuego):
        """
                Determina la mejor acción para Pacman según el algoritmo Minimax.

                Args:
                    estadoJuego: Estado actual del juego.

                Returns:
                    La mejor acción para Pacman según la evaluación Minimax.

                Descripción:
                    Este método utiliza el algoritmo Minimax para calcular la acción óptima para Pacman
                    considerando todas las posibles secuencias de movimientos hasta la profundidad especificada.
        """
        def valorMaximo(estadoJuego, indiceAgente, profundidadActual):
            """
                        Calcula el valor máximo para el agente Pacman en el algoritmo Minimax.

                        Args:
                            estadoJuego: Estado actual del juego.
                            indiceAgente: Índice del agente actual (0 para Pacman).
                            profundidadActual: Profundidad actual en el árbol de búsqueda.

                        Returns:
                            Una tupla (valor, acción) con el valor máximo y la acción asociada.

                        Descripción:
                            Esta función interna calcula el valor máximo para Pacman considerando todas
                            las acciones legales posibles y sus consecuencias.
            """

            # el valor predeterminado es -inf y la acción predeterminada es STOP (es decir, no hacer nada)
            valor = (float("-inf"), Directions.STOP)
            siguienteAgente = (indiceAgente + 1)

            for accion in estadoJuego.getLegalActions(indiceAgente):
                siguienteEstadoJuego = estadoJuego.generateSuccessor(indiceAgente, accion)
                nuevoValor = valorMinimax(siguienteEstadoJuego, siguienteAgente, profundidadActual)

                if nuevoValor > valor[0]:
                    valor = (nuevoValor, accion)

            return valor

        def valorMinimo(estadoJuego, indiceAgente, profundidadActual):
            """
                        Calcula el valor mínimo para los agentes fantasma en el algoritmo Minimax.

                        Args:
                            estadoJuego: Estado actual del juego.
                            indiceAgente: Índice del agente fantasma actual.
                            profundidadActual: Profundidad actual en el árbol de búsqueda.

                        Returns:
                            Una tupla (valor, acción) con el valor mínimo y la acción asociada.

                        Descripción:
                            Esta función interna calcula el valor mínimo para el fantasma considerando todas
                            las acciones legales posibles y sus consecuencias.
                            Reduce la profundidad cuando se completa un ciclo de todos los agentes.
            """

            # Valor predeterminado es +inf y la acción predeterminada es STOP (es decir, no hacer nada)
            valor = (float("inf"), Directions.STOP)
            siguienteAgente = (indiceAgente + 1)

            if siguienteAgente == estadoJuego.getNumAgents():
                siguienteAgente = 0
                profundidadActual -= 1

            for accion in estadoJuego.getLegalActions(indiceAgente):
                siguienteEstadoJuego = estadoJuego.generateSuccessor(indiceAgente, accion)
                nuevoValor = valorMinimax(siguienteEstadoJuego, siguienteAgente, profundidadActual)

                if nuevoValor < valor[0]:
                    valor = (nuevoValor, accion)

            return valor

        def valorMinimax(estadoJuego, indiceAgente, profundidadActual):
            """
                        Calcula el valor Minimax para cualquier agente en el juego.

                        Args:
                            estadoJuego: Estado actual del juego.
                            indiceAgente: Índice del agente actual.
                            profundidadActual: Profundidad actual en el árbol de búsqueda.

                        Returns:
                            El valor numérico según el algoritmo Minimax.

                        Descripción:
                            Esta función recursiva implementa el algoritmo Minimax. Se detiene cuando:
                            - El juego ha terminado (victoria o derrota)
                            - Se alcanza la profundidad máxima de búsqueda
                            Para Pacman (agente 0) calcula el valor máximo, para el fantasma el valor mínimo.
            """
            if estadoJuego.isLose() or estadoJuego.isWin():
                return estadoJuego.getScore()

            if profundidadActual <= 0:
                return self.evaluationFunction(estadoJuego)

            if indiceAgente == 0:
                return valorMaximo(estadoJuego, indiceAgente, profundidadActual)[0]

            else:
                return valorMinimo(estadoJuego, indiceAgente, profundidadActual)[0]

        return valorMaximo(estadoJuego, 0, self.depth)[1]

# python pacman.py -l originalClassic -p MinimaxAgent -a depth=3 -k 1 --frameTime 0.0002 -z 0.5 -a evalFn=better



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
        Agente que utiliza el algoritmo Minimax con poda Alpha-Beta para tomar decisiones.

        Se utiliza el algoritmo Minimax con poda Alpha-Beta, optimizando la búsqueda al eliminar ramas del árbol que no afectarán la decisión final.
    """
    def getAction(self, estadoJuego):
        """
                Determina la mejor acción para Pacman según el algoritmo Alpha-Beta.

                Args:
                    estadoJuego: Estado actual del juego.

                Returns:
                    La mejor acción para Pacman según la evaluación Alpha-Beta.

                Descripción:
                    Este método utiliza el algoritmo Minimax con poda Alpha-Beta para calcular
                    la acción óptima para Pacman de manera más eficiente que el Minimax estándar.

        """
        def valorMaximo(estadoJuego, indiceAgente, profundidadActual, alfa, beta):
            """
                        Calcula el valor máximo con poda Alpha-Beta para el agente Pacman.

                        Args:
                            estadoJuego: Estado actual del juego.
                            indiceAgente: Índice del agente actual (0 para Pacman).
                            profundidadActual: Profundidad actual en el árbol de búsqueda.
                            alfa: Valor alpha actual para la poda.
                            beta: Valor beta actual para la poda.

                        Returns:
                            Una tupla (valor, acción) con el valor máximo y la acción asociada.

                        Descripción:
                            Esta función interna calcula el valor máximo para Pacman con poda Alpha-Beta,
                            evitando explorar ramas que no pueden mejorar el resultado ya encontrado.
            """

            # Valor predeterminado es -inf y la acción predeterminada es STOP (es decir, no hacer nada)
            valor = (float("-inf"), Directions.STOP)
            siguienteAgente = (indiceAgente + 1)

            for accion in estadoJuego.getLegalActions(indiceAgente):
                siguienteEstadoJuego = estadoJuego.generateSuccessor(indiceAgente, accion)
                nuevoValor = valorMinimax(siguienteEstadoJuego, siguienteAgente, profundidadActual, alfa, beta)

                if nuevoValor > valor[0]:
                    valor = (nuevoValor, accion)

                alfa = max(alfa, valor[0])
                if valor[0] > beta:
                    return valor

            return valor

        """
                    Calcula el valor mínimo con poda Alpha-Beta para el agente fantasma.

                    Args:
                        estadoJuego: Estado actual del juego.
                        indiceAgente: Índice del agente fantasma actual.
                        profundidadActual: Profundidad actual en el árbol de búsqueda.
                        alfa: Valor alpha actual para la poda.
                        beta: Valor beta actual para la poda.

                    Returns:
                        Una tupla (valor, acción) con el valor mínimo y la acción asociada.

                    Descripción:
                        Esta función interna calcula el valor mínimo para el fantasma con poda Alpha-Beta,
                        evitando explorar ramas que no pueden mejorar el resultado ya encontrado.
        """
        def valorMinimo(estadoJuego, indiceAgente, profundidadActual, alfa, beta):

            # Valor predeterminado es +inf y la acción predeterminada es STOP (es decir, no hacer nada)
            valor = (float("inf"), Directions.STOP)
            siguienteAgente = (indiceAgente + 1)

            if siguienteAgente == estadoJuego.getNumAgents():
                siguienteAgente = 0
                profundidadActual -= 1

            for accion in estadoJuego.getLegalActions(indiceAgente):
                siguienteEstadoJuego = estadoJuego.generateSuccessor(indiceAgente, accion)
                nuevoValor = valorMinimax(siguienteEstadoJuego, siguienteAgente, profundidadActual, alfa, beta)

                if nuevoValor < valor[0]:
                    valor = (nuevoValor, accion)

                beta = min(beta, valor[0])
                if valor[0] < alfa:
                    return valor

            return valor

        """
                    Calcula el valor Minimax con poda Alpha-Beta para cualquier agente.

                    Args:
                        estadoJuego: Estado actual del juego.
                        indiceAgente: Índice del agente actual.
                        profundidadActual: Profundidad actual en el árbol de búsqueda.
                        alfa: Valor alpha actual para la poda.
                        beta: Valor beta actual para la poda.

                    Returns:
                        El valor numérico según el algoritmo Alpha-Beta.

                    Descripción:
                        Esta función recursiva implementa el algoritmo Minimax con poda Alpha-Beta.
                        Se detiene en las mismas condiciones que el Minimax estándar pero evita
                        explorar ramas que no influirán en la decisión final.
        """
        def valorMinimax(estadoJuego, indiceAgente, profundidadActual, alfa, beta):
            if estadoJuego.isLose() or estadoJuego.isWin():
                return estadoJuego.getScore()

            if profundidadActual <= 0:
                return self.evaluationFunction(estadoJuego)

            if indiceAgente == 0:
                return valorMaximo(estadoJuego, indiceAgente, profundidadActual, alfa, beta)[0]
            else:
                return valorMinimo(estadoJuego, indiceAgente, profundidadActual, alfa, beta)[0]

        return valorMaximo(estadoJuego, 0, self.depth, float("-inf"), float("inf"))[1]
# python pacman.py -l originalClassic -p AlphaBetaAgent -a depth=3 -k 1 --frameTime 0.0002 -z 0.5 -a evalFn=better


# IGUAL QUE EL MINIMAX, PERO HABRIA QUE SUBIR LA MEDIA DE LOS NODOS AL MIN
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
       Agente que utiliza el algoritmo Expectimax para tomar decisiones en entornos probabilísticos.

       Esta clase implementa un agente que utiliza el algoritmo Expectimax, que modela a los fantamas como agentes que actúan aleatoriamente en vez de forma óptima.
    """
    def getAction(self, estadoJuego):
        """
                Determina la mejor acción para Pacman según el algoritmo Expectimax.

                Args:
                    estadoJuego: Estado actual del juego.

                Returns:
                    La mejor acción para Pacman según la evaluación Expectimax.

                Descripción:
                    Este método utiliza el algoritmo Expectimax para calcular la acción óptima para Pacman
                    considerando que los fantasmas pueden moverse aleatoriamente en vez de forma óptima.

        """
        def valorMaximo(estadoJuego, indiceAgente, profundidadActual):
            """
                        Calcula el valor máximo para el agente Pacman en el algoritmo Expectimax.

                        Args:
                            estadoJuego: Estado actual del juego.
                            indiceAgente: Índice del agente actual (0 para Pacman).
                            profundidadActual: Profundidad actual en el árbol de búsqueda.

                        Returns:
                            Una tupla (valor, acción) con el valor máximo y la acción asociada.

                        Descripción:
                            Esta función interna calcula el valor máximo para Pacman considerando todas
                            las acciones legales posibles y sus consecuencias en un contexto probabilístico.
            """
            # Valor predeterminado es -inf y la acción predeterminada es STOP (es decir, no hacer nada)
            valor = (float("-inf"), Directions.STOP)
            siguienteAgente = (indiceAgente + 1)

            for accion in estadoJuego.getLegalActions(indiceAgente):
                siguienteEstadoJuego = estadoJuego.generateSuccessor(indiceAgente, accion)
                nuevoValor = valorExpectimax(siguienteEstadoJuego, siguienteAgente, profundidadActual)

                if nuevoValor > valor[0]:
                    valor = (nuevoValor, accion)

            return valor

        """
                    Calcula el valor esperado para los agentes fantasma en Expectimax.

                    Args:
                        estadoJuego: Estado actual del juego.
                        indiceAgente: Índice del agente fantasma actual.
                        profundidadActual: Profundidad actual en el árbol de búsqueda.

                    Returns:
                        El valor esperado considerando todos los movimientos posibles con igual probabilidad.

                    Descripción:
                        Esta función calcula el valor esperado para los fantasmas asumiendo que eligen
                        aleatoriamente entre todas sus acciones posibles. Devuelve el promedio de los
                        valores resultantes de todas las acciones legales.
        """
        def valorEsperado(estadoJuego, indiceAgente, profundidadActual):
            valores = []
            siguienteAgente = (indiceAgente + 1)

            if siguienteAgente == estadoJuego.getNumAgents():
                siguienteAgente = 0
                profundidadActual -= 1

            for accion in estadoJuego.getLegalActions(indiceAgente):
                siguienteEstadoJuego = estadoJuego.generateSuccessor(indiceAgente, accion)
                nuevoValor = valorExpectimax(siguienteEstadoJuego, siguienteAgente, profundidadActual)
                valores.append(nuevoValor)

            return sum(valores) / len(valores) if valores else 0

        """
                    Calcula el valor Expectimax para cualquier agente en el juego.

                    Args:
                        estadoJuego: Estado actual del juego.
                        indiceAgente: Índice del agente actual.
                        profundidadActual: Profundidad actual en el árbol de búsqueda.

                    Returns:
                        El valor numérico según el algoritmo Expectimax.

                    Descripción:
                        Esta función recursiva implementa el algoritmo Expectimax completo. Para Pacman
                        calcula el máximo valor posible, y para el fantasma calcula el valor esperado
                        asumiendo movimientos aleatorios uniformes.
        """
        def valorExpectimax(estadoJuego, indiceAgente, profundidadActual):
            if estadoJuego.isLose() or estadoJuego.isWin():
                return estadoJuego.getScore()

            if profundidadActual <= 0:
                return self.evaluationFunction(estadoJuego)

            if indiceAgente == 0:
                return valorMaximo(estadoJuego, indiceAgente, profundidadActual)[0]
            else:
                return valorEsperado(estadoJuego, indiceAgente, profundidadActual)

        return valorMaximo(estadoJuego, 0, self.depth)[1]

# python pacman.py -l originalClassic -p ExpectimaxAgent -a depth=3 -k 1 --frameTime 0.0002 -z 0.5 -a evalFn=better


# Hecho en clase con luis gonzaga, heuristica mejorada teniendo en cuenta la distancia del fantamas y la comida mas cercana ç
# para que pacman no se atasque tanto, otra opción viable podría ser implementar A* pero es muy costosa.
def betterEvaluationFunction(currentGameState: GameState) -> float:

    posicionpacman = currentGameState.getPacmanPosition()

    posicioncapsulas = currentGameState.getCapsules()

    posicionfantasma = currentGameState.getGhostPositions()[0]

    numero_capsulas_restantes = len(posicioncapsulas)

    distancia_fantasma = util.manhattanDistance(posicionpacman, posicionfantasma)

    if posicioncapsulas:
        minima_distancia_capsulas = min(util.manhattanDistance(posicionpacman, capsule) for capsule in posicioncapsulas)
    else:
        minima_distancia_capsulas = float('inf')

    value = ( 3 * (1.0 / minima_distancia_capsulas) + -50 * (1.0 / distancia_fantasma) + -10 * numero_capsulas_restantes)

    return value

# Abbreviation
better = betterEvaluationFunction
