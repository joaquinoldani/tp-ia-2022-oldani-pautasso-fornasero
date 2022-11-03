from simpleai import search
from simpleai.search import *
from simpleai.search.viewers import WebViewer, BaseViewer
from itertools import permutations
import pytest

'''     Como vamos a representar el estado del juego

        * Posicion del personaje
        * Cajas
        * Movimientos 
        
        Globales:
        * Paredes
        * Movimientos maximos
        * Objetivos
        
'''

#Estado y globales de ejemplo

# PAREDES = ( tupla de posiciones de las paredes)

# MOVIMIENTOS_MAX = cantidad maxima de movimientos

# OBJETIVOS = ( tupla de posiciones de los objetivos )

# INICIAL = ( Posicion del personaje, Posicion de las cajas, Cantidad de movimientos )


def cajas_adyacentes(posicion, cajas):
    fila_personaje, col_personaje = posicion
    adyacentes = []
    for df, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        fila = fila_personaje + df
        columna = col_personaje + dc
        if (fila, columna) in cajas:
            adyacentes.append((fila, columna))
    return adyacentes


def direccion(coordenada):
    fila, columna = coordenada
    if fila == 1:
        return 'abajo'
    elif fila == -1:
        return 'arriba'
    elif columna == 1:
        return 'derecha'
    elif columna == -1:
        return 'izquierda'


def jugar(paredes, cajas, objetivos, jugador, maximos_movimientos):
    PAREDES = tuple(tuple(pared) for pared in paredes)
    OBJETIVOS = tuple(tuple(objetivo) for objetivo in objetivos)
    
    CAJAS = tuple(tuple(caja) for caja in cajas)
    JUGADOR = jugador
    MOVIMIENTOS_MAX = maximos_movimientos

    INICIAL = (
        JUGADOR, #Posicion del personaje
        CAJAS, #Cajas
        0 #Movimientos máximos
    )

    class Sokoban(SearchProblem):
        
        def cost(self, state1, action, state2):
            return 1

        def is_goal(self, state):
            _, cajas, movimientos = state
            return set(cajas) == set(OBJETIVOS) 

        def actions(self, state):
            posicion, cajas, movimientos = state
            acciones_posibles = [] 
            if movimientos < MOVIMIENTOS_MAX:
                fila_personaje, col_personaje = posicion
                # revisamos las 4 opciones de movimiento
                for df, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    fila = fila_personaje + df
                    columna = col_personaje + dc
                    # chequeamos que la nueva posicion no sea una pared, si lo es no agregamos la accion
                    if (fila, columna) not in PAREDES:
                        if (fila, columna) in cajas:
                            # si la nueva posicion es una caja revisamos que la posicion siguiente no sea una pared o una caja
                            if (fila + df, columna + dc) not in PAREDES and (fila + df, columna + dc) not in cajas:
                                # si eso ocurre podemos mover el personaje Y la caja
                                acciones_posibles.append((direccion((df,dc)), (fila, columna), (fila + df, columna + dc)))
                        else:
                            # si no hay cajas, el personaje se puede mover libremente 
                            acciones_posibles.append((direccion((df,dc)), (fila, columna)))
                
            return acciones_posibles


        def result(self, state, action):
            posicion, cajas, movimientos = state
            cajas_modificable = list(cajas)
            # por cada accion incrementamos la cantidad de movimientos
            movimientos += 1
            
            if action[0]:
                # si la accion tiene un tercer elemento quiere decir que hay que mover una caja 
                if len(action) == 3:
                    cajas_modificable = ((caja if caja != action[1] else action[2]) for caja in cajas_modificable)
                #mientras que el segundo elemento siempre es un movimiento del personaje
                posicion = action[1]
            return (posicion, tuple(tuple(caja) for caja in cajas_modificable), movimientos)

        def heuristic(self, state):
            _, cajas ,_  = state
            # controlamos la cantidad de cajas que estan en los objetivos
            return len(set(OBJETIVOS) - set(cajas))


    problema = Sokoban(INICIAL)
    solucion = astar(problema, graph_search=True)

    acciones_joystick = []
    for action, state in solucion.path():
        if action is not None:
            if len(action) == 3:
                accion_real,_,_ = action
                acciones_joystick.append(accion_real)
            elif len(action) == 2:
                accion_real,_ = action
                acciones_joystick.append(accion_real)

    return acciones_joystick

