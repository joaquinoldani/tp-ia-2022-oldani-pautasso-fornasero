from simpleai.search import *
from itertools import combinations

# La cantidad de cajas y objetivos siempre será la misma, y solo habrá un jugador, como en el juego normal. OK

# No puede haber dos objetos físicos en la misma posición. Se consideran objetos a las paredes, las cajas, y el jugador. Nótese que los objetivos no son objetos físicos, podría el jugador comenzar en la misma posición que un objetivo, o una caja comenzar sobre un objetivo también. OK

# Los objetivos no pueden estar en las mismas posiciones que paredes, porque impedirían ganar. OK

# El juego no debe estar ya ganado. Es decir, las cajas no pueden estar todas ya ubicadas en las posiciones objetivos. Lo que sí está permitido es que algunas cajas comiencen ubicadas sobre objetivos (que puede suceder en el juego real, ya que quizás hay que moverlas para ganar). OK

# Las cajas no deben tener más de una pared adyacente, ya que eso incrementa mucho las chances de que la caja nunca pueda ser movida. Las cajas en los bordes son un caso especial: no deberían tener ninguna pared adyacente, ya que el borde implica que ya tienen una "pared" al lado. OK

# No se pueden ubicar cajas en las esquinas del mapa, ya que nunca podrían ser movidas. OK


tamano_fila, tamano_columna = 5, 5

# Variables = paredes + objetivos + cajas + personaje
PAREDES = ['pared1']
OBJETIVOS = ['objetivo1', 'objetivo2']
CAJAS = ['caja1', 'caja2']
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
    elif elemento in CAJAS or elemento in OBJETIVOS:
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
    
# Restricciones
restricciones = []

# La cantidad de cajas y objetivos siempre será la misma, y solo habrá un jugador, como en el juego normal.
def cantidad_cajas_igual_objetivos(variables, values):
    cantidad_cajas, cantidad_objetivos = 0, 0
    for elemento in variables:
        if elemento in CAJAS:
            cantidad_cajas += 1
        elif elemento in OBJETIVOS:
            cantidad_objetivos += 1
    return cantidad_cajas == cantidad_objetivos

restricciones.append(
    (variables, cantidad_cajas_igual_objetivos)
)

# Los objetivos no pueden estar en las mismas posiciones que paredes, porque impedirían ganar.
def objetivos_mismo_lugar_paredes(variables, values):
    elemento1, elemento2 = variables
    val_elemento1, val_elemento2 = values
    if elemento1 in PAREDES and elemento2 in OBJETIVOS:
        # todo chequear si es == o !=
        return val_elemento1 == val_elemento2
    elif elemento1 in OBJETIVOS and elemento2 in PAREDES:
        # todo chequear si es == o !=
        return val_elemento1 == val_elemento2

for elemento1, elemento2 in combinations(variables,2):
    restricciones.append(
        ((elemento1, elemento2), objetivos_mismo_lugar_paredes)
    )

# Las cajas no deben tener más de una pared adyacente, ya que eso incrementa mucho las chances de que la caja nunca pueda ser movida. Las cajas en los bordes son un caso especial: no deberían tener ninguna pared adyacente, ya que el borde implica que ya tienen una "pared" al lado.

def posiciones_adyacentes(posicion):
    fila_pos, columna_pos = posicion
    adyacentes = []
    for df, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        fila = fila_pos + df
        columna = col_pos + dc
        adyacentes.append((fila, columna))
    return adyacentes

def es_borde(posicion):
    fila, columna = posicion
    return ((fila == 0) or (fila == tamano_fila - 1) or (columna == 0) or (columna == tamano_columna - 1))
        

def cantidad_paredes_adyacentes_caja(variables, values):
    #nos llega una unica posicion
    posicion_caja = values

    posiciones_adyacentes = posiciones_adyacentes(posicion_caja)
    cantidad_paredes = 0
    for posicion in posiciones_adyacentes:
        if posicion in PAREDES or es_borde(posicion):
            cantidad_paredes += 1
    #retornamos si hay dos o mas paredes adyacentes a la posicion
    return cantidad_paredes > 1

for caja in CAJAS:
    restricciones.append(
        (caja, cantidad_paredes_adyacentes_caja)
    )

# El juego no debe estar ya ganado. Es decir, las cajas no pueden estar todas ya ubicadas en las posiciones objetivos. Lo que sí está permitido es que algunas cajas comiencen ubicadas sobre objetivos (que puede suceder en el juego real, ya que quizás hay que moverlas para ganar).

def cajas_puestas_en_objetivos(variables, values):
    cantidad = 0
    for elemento1, elemento2 in combinations(variables, 2):
        val_elemento1, val_elemento2 = values[elemento1], values[elemento2]
    #chequeamos que cada par contenta una caja y un objetivo
    #si los valores son iguales, sumamos una coincidencia
        if elemento1 in OBJETIVOS and elemento2 in CAJAS:
            if val_elemento1 == val_elemento2:
                cantidad += 1
        elif elemento1 in CAJAS and elemento2 in OBJETIVOS:
            if val_elemento1 == val_elemento2:
                cantidad += 1
    # retornamos si la cantidad coincide con las cajas y objetivos a ubicar
    return cantidad == len(CAJAS) == len(OBJETIVOS)

restricciones.append(
    ((CAJAS + OBJETIVOS), cajas_puestas_en_objetivos)
)

# No puede haber dos objetos físicos en la misma posición. Se consideran objetos a las paredes, las cajas, y el jugador. Nótese que los objetivos no son objetos físicos, podría el jugador comenzar en la misma posición que un objetivo, o una caja comenzar sobre un objetivo también.

def cajas_paredes_personaje_mismo_lugar(variables, values):
    elemento1, elemento2 = varibles
    val_elemento1, val_elemento2 = values
    if elemento1 in PAREDES or elemento1 in CAJAS or elemento1 == PERSONAJE:
        if elemento2 in PAREDES or elemento2 in CAJAS or elemento2 == PERSONAJE:
            # todo chequear si es == o !=
            return val_elemento1 == val_elemento2

for elemento1, elemento2 in combinations(variables,2):
    restricciones.append(
        ((elemento1, elemento2), objetivos_mismo_lugar_paredes)
    )

problem = CspProblem(variables, dominio, restricciones)
solution = backtrack(problem)


print(variables)
print(dominio)
print("Solution:")
print(solution)

    
    