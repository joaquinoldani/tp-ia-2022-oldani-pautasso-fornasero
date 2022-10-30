from simpleai import search
from simpleai.search import *
from simpleai.search.viewers import WebViewer, BaseViewer

# '''     Como vamos a representar el estado del juego

#         * Posicion del personaje
#         * Cajas
#         * Objetivos
#         * Movimientos 
        
#         Globales:
#         * Paredes
#         * Movimientos maximos
        
# '''

# Estado y globales de ejemplo

# Estructura de action:
# ((nueva_fila_jugador,nueva_columna_jugador),(nueva_fila_caja,nueva_columna_caja)) <- nueva posicion

# Paredes
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

MOVIMIENTOS_MAX = 300

# Estado inicial
INICIAL = (
    (2,2), # Posicion del personaje
    ((2,3),(3,3),(4,3),(6,1),(6,3),(6,4),(6,5)), # Cajas
    ((2,1),(3,5),(4,1),(5,4),(6,3),(6,6),(7,4)), # Objetivos
    0, # Movimientos
)

def cajas_adyacentes(posicion, cajas):
    fila_personaje, col_personaje = posicion
    adyacentes = []
    # a partir de la posicion del personaje, obtengo todas las 
    # cajas adyacentes
    for df, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        fila = fila_personaje + df
        columna = col_personaje + dc
        if (fila, columna) in cajas:
            adyacentes.append((fila, columna))
    return adyacentes

class Sokoban(SearchProblem):
    
    def cost(self, state1, action, state2):
        # el costo es 1 ya que contabilizamos cantidad de movimientos
        return 1

    def is_goal(self, state):
        _, cajas, objetivos, movimientos = state
        # revisamos que los objetivos tengan cajas encima y que no se hayan excedidos los movimientos
        return sorted(cajas) == sorted(objetivos) and movimientos <= MOVIMIENTOS_MAX

    def actions(self, state):
        posicion, cajas, objetivos, movimientos = state
        acciones_posibles = []
        # verifico que la cantidad de movimientos no exceda el maximo
        if (MOVIMIENTOS_MAX < movimientos):   
            fila_personaje, col_personaje = posicion
            cajas_ady = cajas_adyacentes(posicion, cajas)
            for df, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                fila = fila_personaje + df
                columna = col_personaje + dc
                # si la posicion nueva no es una pared
                if (fila, columna) not in PAREDES:
                    # y ahora verificamos si la posicion nueva es una caja
                    if (fila, columna) in cajas_ady:
                        # verificamos que la posicion siguiente no sea una pared o una caja para hacer el movimiento
                        if (fila + df, columna + dc) not in PAREDES and (fila + df, columna + dc) not in cajas:
                            acciones_posibles.append(('mover_personaje_caja', (fila, columna), (fila + df, columna + dc)))
                    else:
                        acciones_posibles.append(('mover_personaje', (fila, columna), (0,0)))
        return acciones_posibles

    def result(self, state, action):
        state_modificable = [list(fila) for fila in state]
        posicion, cajas, objetivos, movimientos = state_modificable
        if action:
            if action[0] == 'mover_personaje_caja':
                # por cada accion sumo 1 movimiento
                movimientos += 1
                # reemplazo la posicion donde estaba la caja a mover (misma posicion donde se movio el personaje) por la posicion nueva
                cajas.replace(action[1],action[2])
                # muevo el personaje
                posicion = action[1]

            elif action[0] == 'mover_personaje':
                # solo movemos el personaje
                movimientos += 1
                posicion = action[1]

        # rearmo el estado y lo devuelvo
        state_final = []
        state_final.append(posicion)
        state_final.append(cajas)
        state_final.append(objetivos)
        state_final.append(movimientos)
        return tuple(tuple(fila) for fila in state_final)

    def heuristic(self, state):
        posicion, cajas, objetivos, movimientos = state
        return len(set(cajas) - set(objetivos))


problema = astar(Sokoban(INICIAL))
viewer = BaseViewer()

print("Estado meta:")
print(problema.state)

for action, state in problema.path():
    print("Haciendo", action, "llegué a:")
    print(state)

print("Profundidad:", len(list(problema.path())))