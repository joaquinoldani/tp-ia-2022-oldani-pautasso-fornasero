from itertools import combinations
from simpleai.search import (MOST_CONSTRAINED_VARIABLE, CspProblem, backtrack)

# La cantidad de cajas y objetivos siempre será la misma, y solo habrá un jugador, como en el juego normal. OK

# No puede haber dos objetos físicos en la misma posición. Se consideran objetos a las paredes, las cajas, y el jugador. Nótese que los objetivos no son objetos físicos, podría el jugador comenzar en la misma posición que un objetivo, o una caja comenzar sobre un objetivo también. OK

# Los objetivos no pueden estar en las mismas posiciones que paredes, porque impedirían ganar. OK

# El juego no debe estar ya ganado. Es decir, las cajas no pueden estar todas ya ubicadas en las posiciones objetivos. Lo que sí está permitido es que algunas cajas comiencen ubicadas sobre objetivos (que puede suceder en el juego real, ya que quizás hay que moverlas para ganar). OK

# Las cajas no deben tener más de una pared adyacente, ya que eso incrementa mucho las chances de que la caja nunca pueda ser movida. Las cajas en los bordes son un caso especial: no deberían tener ninguna pared adyacente, ya que el borde implica que ya tienen una "pared" al lado. OK

# No se pueden ubicar cajas en las esquinas del mapa, ya que nunca podrían ser movidas. OK

# Caso prueba simple
tamano_fila, tamano_columna = 5, 5
PAREDES = [f'pared{i+1}' for i in range(1)]
OBJETIVOS = [f'objetivo{i+1}' for i in range(2)]
CAJAS = [f'caja{i+1}' for i in range(2)]

# Caso prueba mediano
# tamano_fila, tamano_columna = 7, 7
# PAREDES = [f'pared{i+1}' for i in range(4)]
# OBJETIVOS = [f'objetivo{i+1}' for i in range(3)]
# CAJAS = [f'caja{i+1}' for i in range(3)]

# Caso prueba grande
# tamano_fila, tamano_columna = 11, 10
# PAREDES = [f'pared{i+1}' for i in range(12)]
# OBJETIVOS = [f'objetivo{i+1}' for i in range(7)]
# CAJAS = [f'caja{i+1}' for i in range(7)]

PERSONAJE = ['personaje']

# Variables = paredes + objetivos + cajas + personaje
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
    cajas, objetivos, personaje = variables
    return (len(cajas) == len(objetivos)) and len(personaje) == 1

restricciones.append(
    (CAJAS + OBJETIVOS + PERSONAJE, cantidad_cajas_igual_objetivos)
)

# Los objetivos no pueden estar en las mismas posiciones que paredes, porque impedirían ganar.
def objetivo_mismo_lugar_pared(variables, values):
    elemento1, elemento2 = variables
    val_elemento1, val_elemento2 = values
    # si uno es pared y el otro objeto, preguntamos si estan en la misma posicion
    if (elemento1 in PAREDES and elemento2 in OBJETIVOS) or (elemento1 in OBJETIVOS and elemento2 in PAREDES):
        # todo chequear si es == o !=
        return val_elemento1 != val_elemento2
    # si ambos son pared o ambos objetivos, devolvemos True porque no nos interesan
    elif (elemento1 and elemento2 in OBJETIVOS) or (elemento1 and elemento2 in PAREDES):
        return True

for elemento1, elemento2 in combinations(PAREDES+OBJETIVOS,2):
    restricciones.append(
        ((elemento1, elemento2), objetivo_mismo_lugar_pared)
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
    # armamos una tupla de tuplas con lo que nos llega en variables y values
    # ((elemento1, posicion1), (elemento2, posicion2), ..., (elementoN, posicionN))
    lista_elementos = []
    for index, elemento in enumerate(variables):
        lista_elementos.append((elemento,values[index]))
    #por cada uno de esas combinaciones de elementos, nos guardamos los elementos y su valores
    for objeto1, objeto2 in combinations(lista_elementos, 2):
        elemento1, elemento2 = objeto1[0], objeto2[0]
        val_elemento1, val_elemento2 = objeto1[1], objeto2[1]
    #chequeamos que cada par contenga una caja y un objetivo
    #si los valores son iguales, sumamos una coincidencia ya que estan en el mismo lugar
        if (elemento1 in OBJETIVOS and elemento2 in CAJAS) or (elemento1 in CAJAS and elemento2 in OBJETIVOS):
            if val_elemento1 == val_elemento2:
                cantidad += 1
    # retornamos si la cantidad coincide con las cajas y objetivos a ubicar
    return cantidad == len(CAJAS) == len(OBJETIVOS)

restricciones.append(
    (CAJAS + OBJETIVOS, cajas_puestas_en_objetivos)
)

# No puede haber dos objetos físicos en la misma posición. Se consideran objetos a las paredes, las cajas, y el jugador. Nótese que los objetivos no son objetos físicos, podría el jugador comenzar en la misma posición que un objetivo, o una caja comenzar sobre un objetivo también.

def cajas_paredes_personaje_mismo_lugar(variables, values):
    elemento1, elemento2, elemento3 = variables
    val_elemento1, val_elemento2, val_elemento3 = values
    if elemento1 in PAREDES or elemento1 in CAJAS or elemento1 == PERSONAJE:
        if elemento2 in PAREDES or elemento2 in CAJAS or elemento2 == PERSONAJE:
            if elemento3 in PAREDES or elemento3 in CAJAS or elemento3 == PERSONAJE:
                # todo chequear si es == o !=
                return val_elemento1 != val_elemento2 != val_elemento3

for elemento1, elemento2, elemento3 in combinations(CAJAS+PAREDES+PERSONAJE,3):
    restricciones.append(
        ((elemento1, elemento2, elemento3), cajas_paredes_personaje_mismo_lugar)
    )

# EXTRA
# Los objetivos no pueden estar en las mismas posiciones que otros objetivos.
def objetivos_mismo_lugar(variables, values):
    val_elemento1, val_elemento2 = values
    return val_elemento1 != val_elemento2

for elemento1, elemento2 in combinations(OBJETIVOS,2):
    restricciones.append(
        ((elemento1, elemento2), objetivos_mismo_lugar)
    )

problem = CspProblem(variables, dominio, restricciones)
solution = backtrack(problem, variable_heuristic = MOST_CONSTRAINED_VARIABLE)


print('Variables:',variables)
print('Dominio:',dominio)
for restriccion in restricciones:
    print('Restriccion:', restriccion)
print("Solution:")
print(solution)

    
    