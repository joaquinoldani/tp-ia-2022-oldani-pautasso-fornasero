from simpleai import search
from simpleai.search import *
from simpleai.search.viewers import WebViewer, BaseViewer
from itertools import permutations

'''     Como vamos a representar el estado del juego

        * Posicion del personaje
        * Cajas
        * Objetivos
        * Movimientos 
        
        Globales:
        * Paredes
        * Movimientos maximos
        
'''

#Estado y globales de ejemplo

#Paredes
PAREDES = (
    (0,2),
    (0,3),
    (0,4),
    (0,5),
    (1,0),
    (1,1),
    (1,2),
    (1,6),
    (2,0),
    (2,6),
    (3,0),
    (3,1),
    (3,2),
    (3,6),
    (4,0),
    (4,2),
    (4,3),
    (4,6),
    (5,0),
    (5,2),
    (5,6),
    (5,7),
    (6,0),
    (6,7),
    (7,0),
    (7,7),
    (8,0),
    (8,1),
    (8,2),
    (8,3),
    (8,4),
    (8,5),
    (8,6),
    (8,7),
)

MOVIMIENTOS_MAX = 15

#Estado inicial
INICIAL = (
    (2,2), #Posicion del personaje
    ((2,3),(3,3),(4,3),(6,1),(6,3),(6,4),(6,5)), #Cajas
    ((2,1),(3,5),(4,1),(5,4),(6,3),(6,6),(7,4)), #Objetivos
    0, #Movimientos
)

def cajas_adyacentes(posicion, cajas):
    fila_personaje, col_personaje = posicion
    adyacentes = []
    for df, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        fila = fila_personaje + df
        columna = col_personaje + dc
        if (fila, columna) in cajas:
            adyacentes.append((fila, columna))
    return adyacentes

class Sokoban(SearchProblem):
    
    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        _, cajas, objetivos, movimientos = state
        return sorted(cajas) == sorted(objetivos) and movimientos <= MOVIMIENTOS_MAX

    def actions(self, state):
        #creo q hace falta ver si no me paso de los movimientos maximos
        acciones_posibles = []
        posicion, cajas, objetivos, movimientos = state
        fila_personaje, col_personaje = posicion
        cajas_ady = cajas_adyacentes(posicion, cajas)
        for df, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            fila = fila_personaje + df
            columna = col_personaje + dc
            if (fila, columna) not in PAREDES:
                if (fila, columna) in cajas_ady:
                    if (fila + df, columna + dc) not in PAREDES and (fila + df, columna + dc) not in cajas:
                        acciones_posibles.append(('mover', (fila, columna), (fila + df, columna + dc)))
                else:
                    acciones_posibles.append(('mover', (fila, columna)))
        return acciones_posibles

    def result(self, state, action):
        posicion, cajas, objetivos, movimientos = state
        if action[0] == 'mover':
            movimientos += 1
            if len(action) == 3:
                cajas = tuple((caja if caja != action[1] else action[2]) for caja in cajas)
            posicion = action[1]
        return (posicion, cajas, objetivos, movimientos)

    def heuristic(self, state):
        posicion, cajas, objetivos, movimientos = state
        return len(set(cajas) - set(objetivos))


problema = Sokoban(INICIAL)
solucion = astar(problema, graph_search=True)

for accion, estado in solucion.path():
    print("Action:", accion, "Pendientes:", estado[1])