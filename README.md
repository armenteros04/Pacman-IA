<img src="https://eps.ujaen.es/sites/centro_eps/files/styles/news_photo_tablet/public/uploads/node_noticia/2020-03/unnamed.png?itok=gtl_-LKj" width="150" height="90" />

# Pacman IA
## Proyecto de prácticas de Inteligencia Artificial
### Realizado por Antonio Armenteros y Manuel Serrano

En este proyecto realizado para las prácticas de IA, hemos usado un recurso de la Universidad de Berkeley en California. 
Hemos implementado un Pacman que puede realizar búsquedas tanto DFS, BFS como A*. 

También hemos conseguido desarrollador el algoritmo MINIMAX, EXPECTIMAX y MINIMAX con poda alfa beta. El punto de partida de los archivos de código y los layouts ha sido desarrollado por [John DeNero](https://denero.org/) y [Dan Klein](https://people.eecs.berkeley.edu/~klein/)



[Pulsando en este enlace](https://ai.berkeley.edu/project_overview.html) se puede ver en más detalle toda la información y una descripción general de todo el proyecto al completo.

<img src="https://ai.berkeley.edu/images/pacman_game.gif">


## **Información importante**

Para ejecutar una partida de pacman basta con poner en una terminal lo siguiente:
```
python pacman.py
```
Si queremos ejecutar una partida pero cambiar el layout habrá que especificarlo de la siguiente manera:
```
python pacman.py --layout nombreLayout 
```
Si queremos ejecutar una partida con un agente en concreto se pondrá de la siguiente manera:
```
python pacman.py  --pacman nombreAgente
```
Si queremos ejecutar una partida sobre teoría de juegos y aplicar por ejemplo un algoritmo ExpectiMax sería de la siguiente manera indicando la profundidad:
```
python pacman.py -l originalClassic -p ExpectimaxAgent -a depth=3
```
Todos estos parametros se pueden combinar entre sí, por ejemplo en la siguiente ejecución muestro un ejemplo de como cambiar el zoom, el tiempo de frames, el agente y el layout:
```
python pacman.py --layout testMaze --pacman GoWestAgent -z 0.5 --frameTime 0.5
```
Otro ejemplo combinando varios parámetros:
```
python pacman.py -l originalClassic -p MinimaxAgent -a depth=3 -k 1 --frameTime 0.02 -z 0.5 -a evalFn=better
```
Finalemente si quieres explorar más parámetros o información necesaria para una ejecución en concreto puedes usar lo siguiente:
```
python pacman.py -h
```

## **Fichero search.py en /exploracionbusqueda**

En este fichero se encuentra el código implementado de la búsqueda DFS y A*.

**Pseudocódigo DFS**
```
función depthFirstSearch(problem):
    pila = nueva pila vacía
    visitados = conjunto vacío
    movimientos = lista vacía
    cantidad_depasos = 0

    pila.push((problem.getStartState(), lista vacía))

    mientras pila no esté vacía:
        estado, camino = pila.pop()

        si problem.isGoalState(estado):
            celdas_visitadas = tamaño de visitados
            si celdas_visitadas > 0:
                ratio_repeticion = cantidad_depasos / celdas_visitadas
            sino:
                ratio_repeticion = 0
            retornar camino

        si estado no está en visitados:
            agregar estado a visitados
            cantidad_depasos = cantidad_depasos + 1
            para cada sucesor, accion, _ en problem.getSuccessors(estado):
                si sucesor no está en visitados:
                    pila.push((sucesor, camino + [accion]))
                    agregar accion a movimientos

    retornar lista vacía
```

**Pseudocódigo A**
```
función aStarSearch(problem, heuristic):
    colaprioridad = nueva cola de prioridad
    inicio = problem.getStartState()
    colaprioridad.push((inicio, lista vacía, 0), heuristic(inicio, problem))
    visitadas = diccionario vacío
    celdas_visitadas = conjunto vacío

    mientras colaprioridad no esté vacía:
        current_state, acciones, costetotal = colaprioridad.pop()

        si problem.isGoalState(current_state):
            pasos = longitud de acciones
            si no acciones:
                celdas_unicas = False
            sino:
                celdas_unicas = longitud de acciones
            si pasos > 0:
                ratio_repeticion = pasos / celdas_unicas
            sino:
                ratio_repeticion = 0
            retornar acciones

        si current_state no está en visitadas o costetotal < visitadas[current_state]:
            visitadas[current_state] = costetotal
            agregar current_state a celdas_visitadas

            para cada successor, action, step_cost en problem.getSuccessors(current_state):
                coste = costetotal + step_cost
                prioridad = coste + heuristic(successor, problem)
                new_actions = acciones + [action]
                colaprioridad.push((successor, new_actions, coste), prioridad)

    retornar lista vacía

```


Además hay un método de exploración el cual emplea backtracking para explorar el mapa por completo sin dejarse ninguna casilla sin visitar.

**Pseudocódigo Exploración**
```
función exploracionterca(problem):
    visitadas = conjunto vacío
    pila_movimientos = nueva pila
    movimientos = lista vacía

    estado_inicial = problem.getStartState()
    agregar estado_inicial a visitadas
    pila_movimientos.push((estado_inicial, ninguno))

    mientras pila_movimientos no esté vacía:
        estado_actual, accion_anterior = pila_movimientos.pop()

        si accion_anterior:
            agregar accion_anterior a movimientos
            pila_movimientos.push((estado_actual, accion_anterior))

        vecinos_legales = Actions.getLegalNeighbors(estado_actual, problem.walls)
        hay_movimiento = falso

        para cada sucesor, accion, _ en problem.getSuccessors(estado_actual):
            si sucesor no está en visitadas y sucesor está en vecinos_legales:
                agregar sucesor a visitadas
                pila_movimientos.push((sucesor, accion))
                hay_movimiento = verdadero
                romper

        mientras no hay_movimiento y pila_movimientos no esté vacía:
            estado_previo, accion_reversa = pila_movimientos.pop()
            agregar Directions.REVERSE[accion_reversa] a movimientos

            si pila_movimientos está vacía:
                pila_movimientos.push((problem.__getstate__()["startState"], ninguno))
                estado_actual, accion_anterior = pila_movimientos.pop()

                si accion_anterior:
                    agregar accion_anterior a movimientos
                    pila_movimientos.push((estado_actual, accion_anterior))

                vecinos_legales = Actions.getLegalNeighbors(estado_actual, problem.walls)
                hay_movimiento = falso

                para cada sucesor, accion, _ en problem.getSuccessors(estado_actual):
                    si sucesor no está en visitadas y sucesor está en vecinos_legales:
                        agregar sucesor a visitadas
                        pila_movimientos.push((sucesor, accion))
                        hay_movimiento = verdadero
                        romper

            para cada sucesor, accion, _ en problem.getSuccessors(estado_previo):
                si sucesor no está en visitadas:
                    agregar sucesor a visitadas
                    pila_movimientos.push((estado_previo, accion_reversa))
                    pila_movimientos.push((sucesor, accion))
                    eliminar último elemento de movimientos
                    hay_movimiento = verdadero
                    romper

    cantidad_pasos = longitud de movimientos
    celdas_visitadas = tamaño de visitadas
    si celdas_visitadas > 0:
        ratio_repeticion = cantidad_pasos / celdas_visitadas
    sino:
        ratio_repeticion = 0

    retornar movimientos
```

## **Fichero searchAgents.py en /exploracionbusqueda**

En este fichero se encuentra el código de los agentes implementados junto con su heurística, problema y búsqueda a realizar.

## **Fichero submission.py en /teoriadejuegos**

En este fichero se encuentra el código implementado del algoritmo MINIMAX, EXPECTIMAX y MINIMAX con poda alfa beta.

**Pseudocódigo MINIMAX**
```
FUNCIÓN getAction(estadoJuego):
    FUNCIÓN valorMaximo(estadoJuego, indiceAgente, profundidadActual):
        valor = (-inf, STOP)
        siguienteAgente = indiceAgente + 1
        PARA cada accion EN estadoJuego.getLegalActions(indiceAgente):
            siguienteEstadoJuego = estadoJuego.generateSuccessor(indiceAgente, accion)
            nuevoValor = valorMinimax(siguienteEstadoJuego, siguienteAgente, profundidadActual)
            SI nuevoValor > valor[0]:
                valor = (nuevoValor, accion)
        RETORNAR valor

    FUNCIÓN valorMinimo(estadoJuego, indiceAgente, profundidadActual):
        valor = (inf, STOP)
        siguienteAgente = indiceAgente + 1
        SI siguienteAgente == estadoJuego.getNumAgents():
            siguienteAgente = 0
            profundidadActual = profundidadActual - 1
        PARA cada accion EN estadoJuego.getLegalActions(indiceAgente):
            siguienteEstadoJuego = estadoJuego.generateSuccessor(indiceAgente, accion)
            nuevoValor = valorMinimax(siguienteEstadoJuego, siguienteAgente, profundidadActual)
            SI nuevoValor < valor[0]:
                valor = (nuevoValor, accion)
        RETORNAR valor

    FUNCIÓN valorMinimax(estadoJuego, indiceAgente, profundidadActual):
        SI estadoJuego.isLose() O estadoJuego.isWin():
            RETORNAR estadoJuego.getScore()
        SI profundidadActual <= 0:
            RETORNAR self.evaluationFunction(estadoJuego)
        SI indiceAgente == 0:
            RETORNAR valorMaximo(estadoJuego, indiceAgente, profundidadActual)[0]
        SINO:
            RETORNAR valorMinimo(estadoJuego, indiceAgente, profundidadActual)[0]

    RETORNAR valorMaximo(estadoJuego, 0, self.depth)[1]
```

**Pseudocódigo EXPECTIMAX**
```
FUNCIÓN getAction(estadoJuego):
    FUNCIÓN valorMaximo(estadoJuego, indiceAgente, profundidadActual):
        valor = (-inf, STOP)
        siguienteAgente = indiceAgente + 1
        PARA cada accion EN estadoJuego.getLegalActions(indiceAgente):
            siguienteEstadoJuego = estadoJuego.generateSuccessor(indiceAgente, accion)
            nuevoValor = valorExpectimax(siguienteEstadoJuego, siguienteAgente, profundidadActual)
            SI nuevoValor > valor[0]:
                valor = (nuevoValor, accion)
        RETORNAR valor

    FUNCIÓN valorEsperado(estadoJuego, indiceAgente, profundidadActual):
        valores = []
        siguienteAgente = indiceAgente + 1
        SI siguienteAgente == estadoJuego.getNumAgents():
            siguienteAgente = 0
            profundidadActual = profundidadActual - 1
        PARA cada accion EN estadoJuego.getLegalActions(indiceAgente):
            siguienteEstadoJuego = estadoJuego.generateSuccessor(indiceAgente, accion)
            nuevoValor = valorExpectimax(siguienteEstadoJuego, siguienteAgente, profundidadActual)
            valores.append(nuevoValor)
        RETORNAR sum(valores) / len(valores) SI valores SINO 0

    FUNCIÓN valorExpectimax(estadoJuego, indiceAgente, profundidadActual):
        SI estadoJuego.isLose() O estadoJuego.isWin():
            RETORNAR estadoJuego.getScore()
        SI profundidadActual <= 0:
            RETORNAR self.evaluationFunction(estadoJuego)
        SI indiceAgente == 0:
            RETORNAR valorMaximo(estadoJuego, indiceAgente, profundidadActual)[0]
        SINO:
            RETORNAR valorEsperado(estadoJuego, indiceAgente, profundidadActual)

    RETORNAR valorMaximo(estadoJuego, 0, self.depth)[1]
```

**Pseudocódigo MINIMAX con poda alfa beta**
```
FUNCIÓN getAction(estadoJuego):
    FUNCIÓN valorMaximo(estadoJuego, indiceAgente, profundidadActual, alfa, beta):
        valor = (-inf, STOP)
        siguienteAgente = indiceAgente + 1
        PARA cada accion EN estadoJuego.getLegalActions(indiceAgente):
            siguienteEstadoJuego = estadoJuego.generateSuccessor(indiceAgente, accion)
            nuevoValor = valorMinimax(siguienteEstadoJuego, siguienteAgente, profundidadActual, alfa, beta)
            SI nuevoValor > valor[0]:
                valor = (nuevoValor, accion)
            alfa = max(alfa, valor[0])
            SI valor[0] > beta:
                RETORNAR valor
        RETORNAR valor

    FUNCIÓN valorMinimo(estadoJuego, indiceAgente, profundidadActual, alfa, beta):
        valor = (inf, STOP)
        siguienteAgente = indiceAgente + 1
        SI siguienteAgente == estadoJuego.getNumAgents():
            siguienteAgente = 0
            profundidadActual = profundidadActual - 1
        PARA cada accion EN estadoJuego.getLegalActions(indiceAgente):
            siguienteEstadoJuego = estadoJuego.generateSuccessor(indiceAgente, accion)
            nuevoValor = valorMinimax(siguienteEstadoJuego, siguienteAgente, profundidadActual, alfa, beta)
            SI nuevoValor < valor[0]:
                valor = (nuevoValor, accion)
            beta = min(beta, valor[0])
            SI valor[0] < alfa:
                RETORNAR valor
        RETORNAR valor

    FUNCIÓN valorMinimax(estadoJuego, indiceAgente, profundidadActual, alfa, beta):
        SI estadoJuego.isLose() O estadoJuego.isWin():
            RETORNAR estadoJuego.getScore()
        SI profundidadActual <= 0:
            RETORNAR self.evaluationFunction(estadoJuego)
        SI indiceAgente == 0:
            RETORNAR valorMaximo(estadoJuego, indiceAgente, profundidadActual, alfa, beta)[0]
        SINO:
            RETORNAR valorMinimo(estadoJuego, indiceAgente, profundidadActual, alfa, beta)[0]

    RETORNAR valorMaximo(estadoJuego, 0, self.depth, -inf, inf)[1]
```