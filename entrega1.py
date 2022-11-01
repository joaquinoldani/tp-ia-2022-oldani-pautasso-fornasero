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

# PAREDES = (
#     (0,0),
#     (0,1),
#     (0,2),
#     (0,3),
#     (0,4),
#     (0,5),
#     (1,0),
#     (1,5),
#     (2,0),
#     (2,1),
#     (2,2),
#     (2,3),
#     (2,4),
#     (2,5)
# )

MOVIMIENTOS_MAX = 30

OBJETIVOS = (
    (5,4), (4,1)
)

# OBJETIVOS = (
#     (1,4), (1,1)
# )

#Estado inicial
INICIAL = (
    (2,2), #Posicion del personaje
    ((2,3),(6,1)), #Cajas
    0, #Movimientos
)

# INICIAL = (
#     (1,2), #Posicion del personaje
#     ((1,3), (1,1)), #Cajas
#     0, #Movimientos
# )

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
        return set(cajas) == set(OBJETIVOS) 

    def actions(self, state):
        #creo q hace falta ver si no me paso de los movimientos maximos
        posicion, cajas, movimientos = state
        acciones_posibles = [] 
        if movimientos < MOVIMIENTOS_MAX:
            fila_personaje, col_personaje = posicion
            cajas_ady = cajas_adyacentes(posicion, cajas)
            # print('Estoy en :', fila_personaje, col_personaje)
            # print('Cajas', cajas)
            # print('Cajas adyacentes: ', cajas_ady)
            for df, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                fila = fila_personaje + df
                columna = col_personaje + dc
                #('Me puedo mover a esto?', fila, columna)
                if (fila, columna) not in PAREDES:
                    if (fila, columna) in cajas:
                        #('Hay una caja adyacente en', fila, columna)
                        if (fila + df, columna + dc) not in PAREDES and (fila + df, columna + dc) not in cajas:
                            #('Puedo empujar la caja a', fila + df, columna + dc)
                            acciones_posibles.append(('mover', (fila, columna), (fila + df, columna + dc)))
                    else:
                        #('En esta posicion no hay nada', fila, columna)
                        acciones_posibles.append(('mover', (fila, columna)))
            
            

        #(acciones_posibles)
        #('----')
        return acciones_posibles

    def result(self, state, action):
        ##(action)
        posicion, cajas, movimientos = state
        cajas_modificable = list(cajas)
        movimientos += 1
        if action[0] == 'mover':
            if len(action) == 3:
                cajas_modificable = ((caja if caja != action[1] else action[2]) for caja in cajas_modificable)
            posicion = action[1]
        return (posicion, tuple(tuple(caja) for caja in cajas_modificable), movimientos)

    def heuristic(self, state):
        _, cajas ,_  = state
        return len(set(OBJETIVOS) - set(cajas))


problema = Sokoban(INICIAL)

solucion = astar(problema)


for accion, estado in solucion.path():
    print("Action:", accion, "Cajas:", estado[1])