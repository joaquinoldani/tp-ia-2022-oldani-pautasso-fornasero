import datetime
import random

from simpleai.search import *
from simpleai.search.csp import _find_conflicts

# La cantidad de cajas y objetivos siempre será la misma, y solo habrá un jugador, como en el juego normal.

# No puede haber dos objetos físicos en la misma posición. Se consideran objetos a las paredes, las cajas, y el jugador. Nótese que los objetivos no son objetos físicos, podría el jugador comenzar en la misma posición que un objetivo, o una caja comenzar sobre un objetivo también.

# Los objetivos no pueden estar en las mismas posiciones que paredes, porque impedirían ganar.

# El juego no debe estar ya ganado. Es decir, las cajas no pueden estar todas ya ubicadas en las posiciones objetivos. Lo que sí está permitido es que algunas cajas comiencen ubicadas sobre objetivos (que puede suceder en el juego real, ya que quizás hay que moverlas para ganar).

# Las cajas no deben tener más de una pared adyacente, ya que eso incrementa mucho las chances de que la caja nunca pueda ser movida. Las cajas en los bordes son un caso especial: no deberían tener ninguna pared adyacente, ya que el borde implica que ya tienen una "pared" al lado.

# No se pueden ubicar cajas en las esquinas del mapa, ya que nunca podrían ser movidas.


tamano_fila, tamano_columna = 5, 5

# Variables = paredes + objetivos + cajas + personaje
PAREDES = ['pared1', 'pared2']
OBJETIVOS = ['objetivo1', 'objetivo2', 'objetivo3']
CAJAS = ['caja1', 'caja2', 'caja3']
PERSONAJE = ['personaje']
variables = PAREDES + OBJETIVOS + CAJAS + PERSONAJE

# Dominios
dominio = {}
for elemento in variables:
    # armarmos los dominios para las paredes y el personaje (pueden ocupar cualquier lugar que no sea borde)
    if elemento in PAREDES or elemento in PERSONAJE:
        dominio[elemento] = []
        # obtenemos la grilla sin los bordes
        for fila in range(tamano_fila):
            for columna in range(tamano_columna):
                #chequeamos los bordes de la grilla
                if (fila == 0) or (fila == tamano_fila - 1) or (columna == 0) or (columna == tamano_columna - 1):
                    continue
                else:
                    dominio[elemento].append((fila,columna))

    # armarmos los dominios para las cajas (pueden ocupar cualquier lugar que no sea borde y no sea esquina)
    elif elemento in CAJAS:
        dominio[elemento] = []
        # obtenemos la grilla sin los bordes
        for fila in range(tamano_fila):
            for columna in range(tamano_columna):
                #chequeamos los bordes de la grilla
                if (fila == 0) or (fila == tamano_fila - 1) or (columna == 0) or (columna == tamano_columna - 1):
                    continue
                # chequeamos las esquinas
                elif (fila == 1 and columna == 1) or (fila == 1 and columna == tamano_columna - 2) or (columna == tamano_columna - 2 and fila == 1) or (columna == tamano_columna - 2 and fila == tamano_fila - 2):
                    continue
                else:
                    dominio[elemento].append((fila,columna))
    

