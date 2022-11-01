from simpleai import search
from simpleai.search import *
from simpleai.search.viewers import WebViewer, BaseViewer
from itertools import permutations

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

#Paredes
PAREDES = (
    (0,2),
    (0,3),
    (0,4),
    (0,5),
    (0,6),
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

MOVIMIENTOS_MAX = 20

OBJETIVOS = (
    (2,1),(3,5),(4,1),(5,4),(6,3),(6,6),(7,4) 
)

#Estado inicial
INICIAL = (
    (1,3), #Posicion del personaje
    (   
    #(2,3),(3,4),(4,4),(6,1),(6,3),(6,4),(6,5)
    (2,1),(3,5),(4,1),(5,4),(6,3),(7,3),(6,6)
    ), #Cajas
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
        _, cajas, movimientos = state
        #print(sorted(cajas))
        #print(sorted(OBJETIVOS))
        #print('---')
        return sorted(cajas) == sorted(OBJETIVOS)

    def actions(self, state):
        #creo q hace falta ver si no me paso de los movimientos maximos
        posicion, cajas, movimientos = state
        acciones_posibles = [] 
    
        fila_personaje, col_personaje = posicion
        print('estoy aca guachin', fila_personaje, col_personaje)
        cajas_ady = cajas_adyacentes(posicion, cajas)
        #obtenemos las posiciones adyacentes a donde esta el personaje
        if movimientos < MOVIMIENTOS_MAX:
            #print('Movimientos: ', movimientos)
            for df, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                fila = fila_personaje + df
                columna = col_personaje + dc
                if (fila, columna) not in PAREDES:
                    if (fila, columna) in cajas_ady:
                        #nos fijamos una posicion mas alla de la caja en busca de una caja o una pared
                        if (fila + df, columna + dc) not in PAREDES and (fila + df, columna + dc) not in cajas:
                            #movemos personaje y caja
                            print('Accion realizada: ',('mover', (fila, columna), (fila + df, columna + dc)))
                            acciones_posibles.append(('mover', (fila, columna), (fila + df, columna + dc)))
                    else:
                        #movemos solo el personaje porque estaba vacio
                        acciones_posibles.append(('mover', (fila, columna)))
        return acciones_posibles

    def result(self, state, action):
        #print(state,action)
        posicion, cajas, movimientos = state
        if action[0] == 'mover':
            movimientos += 1
            #si la accion traia la accion y dos posiciones tenemos que mover personaje y caja
            if len(action) == 3:
                cajas = tuple((caja if caja != action[1] else action[2]) for caja in cajas)
            #sino solo movemos personaje
            posicion = action[1]
        return (posicion, cajas, movimientos)

    def heuristic(self, state):
        _, cajas, _ = state
        #print('Heuristica: ', len(set(OBJETIVOS) - set(cajas)))
        return len(set(OBJETIVOS) - set(cajas))


problema = Sokoban(INICIAL)
viewer = WebViewer()
solucion = astar(problema)

for action, estado in solucion.path():
    print("Action: ", action, "Cajas:", estado[1])