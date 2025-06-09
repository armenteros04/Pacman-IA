# search.py




import sys
from game import Directions, Actions, Agent
from util import  Stack
import util
from game import Directions
from typing import List
from queue import PriorityQueue


args = sys.argv  # Obtener argunmentos de consola


if "--layout" in args:  # Buscar y mostrar nombre
        index = args.index("--layout") + 1
        if index < len(args):
            layout = args[index]


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """

        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Realiza una búsqueda en profundidad (DFS) para encontrar un camino hacia el primer pellet de comida.
    """
    pila = Stack()  # Usamos una pila para DFS
    visitados = set()  # Conjunto de nodos visitados
    movimientos = []  # Para almacenar los movimientos realizados
    cantidad_depasos=0
    # Inicializa la pila con el estado inicial y un camino vacío
    pila.push((problem.getStartState(), []))

    while not pila.isEmpty():
        estado, camino = pila.pop()  # Extrae el nodo más reciente

        # Verifica si el estado es el objetivo (es decir, una posición con comida)
        if problem.isGoalState(estado):
            # Calcular estadísticas

            celdas_visitadas = len(visitados)  # Contamos las celdas únicas visitadas
            ratio_repeticion = cantidad_depasos / celdas_visitadas if celdas_visitadas > 0 else 0

            # Mostrar estadísticas
            print(f"\n---------------------------------------")
            print(f"Estadísticas finales laberinto {layout}")
            print(f"---------------------------------------")
            print(f"Cantidad de pasos realizados -> {cantidad_depasos:}")
            print(f"Número de celdas únicas visitadas -> {celdas_visitadas}")
            print(f"Ratio de repetición -> {ratio_repeticion:.3f}")
            print(f"---------------------------------------")
            print(f"\n")

            return camino  # Devuelve el camino hasta el objetivo

        # Si el estado no ha sido visitado
        if estado not in visitados:
            visitados.add(estado)  # Marca el estado como visitado
            cantidad_depasos+=1
            # Expande los sucesores
            for sucesor, accion, _ in problem.getSuccessors(estado):
                if sucesor not in visitados:
                    pila.push((sucesor, camino + [accion]))  # Agrega los sucesores no visitados a la pila
                    movimientos.append(accion)  # Agrega la acción al listado de movimientos

    # Si no encuentra el camino, devuelve una lista vacía
    return []

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0








def aStarSearch(problem, heuristic=lambda state, problem: 0):
    """
    Implementación de la búsqueda A* (BAE)
    """
    colaprioridad = util.PriorityQueue()
    inicio = problem.getStartState()
    colaprioridad.push((inicio, [], 0), heuristic(inicio, problem))  # (estado, acciones, costo acumulado), prioridad
    visitadas = {}

    celdas_visitadas = set()

    while not colaprioridad.isEmpty():
        current_state, acciones, costetotal = colaprioridad.pop()

        if problem.isGoalState(current_state):
            pasos = len(acciones)
            celdas_unicas =  not acciones or len(acciones) # Celdas únicas visitadas
            ratio_repeticion = pasos / celdas_unicas if pasos > 0 else 0

            # Mostrar estadísticas
            print(f"\n---------------------------------------")
            print(f"Estadísticas finales laberinto {layout}")
            print(f"---------------------------------------")
            print(f"Cantidad de pasos realizados -> {pasos}")
            print(f"Número de celdas únicas visitadas -> {celdas_unicas}")
            print(f"Ratio de repetición -> {ratio_repeticion:.3f}")
            print(f"---------------------------------------\n")

            return acciones

        if current_state not in visitadas or costetotal < visitadas[current_state]:
            visitadas[current_state] = costetotal
            celdas_visitadas.add(current_state)

            for successor, action, step_cost in problem.getSuccessors(current_state):
                coste = costetotal + step_cost
                priority = coste + heuristic(successor, problem)
                new_actions = acciones + [action]
                colaprioridad.push((successor, new_actions, coste), priority)

    return []



def exploracionterca(problem: SearchProblem) -> List[Directions]:
    visitadas = set()  # Celdas visitadas
    pila_movimientos = Stack()  # Pila de estados y movimientos
    movimientos = []  # Lista de acciones realizadas



    estado_inicial = problem.getStartState()
    print("Estado inicial: ", estado_inicial)

    visitadas.add(estado_inicial)
    pila_movimientos.push((estado_inicial, None))  # Estado y acción previa

    while not pila_movimientos.isEmpty():
        estado_actual, accion_anterior = pila_movimientos.pop()
        print(f"Explorando: {estado_actual}")

        if accion_anterior:
            movimientos.append(accion_anterior)
            pila_movimientos.push((estado_actual, accion_anterior))

        vecinos_legales = Actions.getLegalNeighbors(estado_actual, problem.walls)
        hay_movimiento = False

        for sucesor, accion, _ in problem.getSuccessors(estado_actual):
            if sucesor not in visitadas and sucesor in vecinos_legales:
                visitadas.add(sucesor)
                pila_movimientos.push((sucesor, accion))
                hay_movimiento = True
                break

        # Si no hay movimientos, hacemos backtracking hasta encontrar una nueva ruta
        while not hay_movimiento and not pila_movimientos.isEmpty():
            estado_previo, accion_reversa = pila_movimientos.pop()
            movimientos.append(Directions.REVERSE[accion_reversa])
            print(f"Estado previo: {estado_previo}, Acción reversa: {accion_reversa}")  # Imprime la información

            if pila_movimientos.isEmpty():#gestion si se acaba la pila y sigue habiendo cassillas no visitadas alrededor
                pila_movimientos.push((problem.__getstate__()["startState"], None))#usamos el diccionario para empujar el estado actual

                estado_actual, accion_anterior = pila_movimientos.pop()

                if accion_anterior:#replicamos logica pero para hacer un solo movimietnoq que lo saque del problema de estar con la pila vacia cuando aun no ha termiando de explorar
                    movimientos.append(accion_anterior)
                    pila_movimientos.push((estado_actual, accion_anterior))

                vecinos_legales = Actions.getLegalNeighbors(estado_actual, problem.walls)
                hay_movimiento = False

                for sucesor, accion, _ in problem.getSuccessors(estado_actual):
                    if sucesor not in visitadas and sucesor in vecinos_legales:
                        visitadas.add(sucesor)
                        pila_movimientos.push((sucesor, accion))
                        hay_movimiento = True
                        break

            # Buscar una nueva ruta desde estado_previo
            for sucesor, accion, _ in problem.getSuccessors(estado_previo):
                if sucesor not in visitadas:
                    visitadas.add(sucesor)
                    pila_movimientos.push((estado_previo, accion_reversa))#restauramos la pila para no perder el movimietno sacado para echar atras
                    pila_movimientos.push((sucesor, accion))#metemos la accion de salida del backtracking
                    movimientos.pop()  # Cancelamos el último retroceso porque encontramos un nuevo camino
                    hay_movimiento = True
                    break

    cantidad_pasos = len(movimientos)
    celdas_visitadas = len(visitadas)
    ratio_repeticion = cantidad_pasos / celdas_visitadas if celdas_visitadas > 0 else 0


    print(f"\n---------------------------------------")
    print(f"Estadísticas finales laberinto {layout}")
    print(f"---------------------------------------")
    print(f"Cantidad de pasos realizados -> {cantidad_pasos}")
    print(f"Número de celdas únicas visitadas -> {celdas_visitadas}")
    print(f"Ratio de repetición -> {ratio_repeticion:.3f}")
    print(f"---------------------------------------")
    print(f"\n")

    return movimientos




# Done
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
