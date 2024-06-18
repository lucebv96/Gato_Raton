"""
Juego del Gato y el Ratón:

¡Bienvenido al juego del Gato y el Ratón!
En este juego, el objetivo del Gato es atrapar al Ratón antes de que este último llegue a su madriguera.
Por otro lado, el Ratón intenta llegar a salvo a su madriguera sin ser atrapado por el Gato.

Reglas del juego:
1. El juego se desarrolla en un tablero cuadrado de tamaño fijo.
2. El Gato y el Ratón se mueven por turnos.
3. Cada turno, el Gato y el Ratón pueden moverse una casilla en las direcciones: arriba, abajo, izquierda o derecha.
4. El juego termina cuando el Ratón alcanza su madriguera (Ratón gana) o el Gato atrapa al Ratón (Gato gana).
5. El gato tiene una cantidad de movimientos limitada para alcanzar al Ratón

A tener en cuenta:
- El Gato es representado por la letra 'G' en el tablero.
- El Ratón es representado por la letra 'R' en el tablero.
- La madriguera del Ratón es representada por la letra 'M' en el tablero.
- Las casillas vacías se representan con '-' en el tablero.

"""



import random

# --------------> CONDICIONES INICIALES <---------------

#                                                                                                                 Definición del tablero
TAMANO_TABLERO = 5
tablero = [[0 for _ in range(TAMANO_TABLERO)] for _ in range(TAMANO_TABLERO)]

#                                                                                                      Posición de la madriguera del ratón
madriguera_raton = (0, 2)

#                                                                                                   Posiciones iniciales del gato y el ratón
while True:
    pos_gato = (random.randint(0, TAMANO_TABLERO - 1), random.randint(0, TAMANO_TABLERO - 1))
    if pos_gato != madriguera_raton:
        break

while True:
    pos_raton = (random.randint(0, TAMANO_TABLERO - 1), random.randint(0, TAMANO_TABLERO - 1))
    if pos_raton != madriguera_raton and pos_raton != pos_gato:
        break



# --------------> MOVIMIENTOS <---------------


#                                                                    Movimientos posibles del gato y ratón (Arriba, abajo, izquierda, derecha)
movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

#                                                                                                                       Funciones auxiliares
def es_posicion_valida(x, y):
    return 0 <= x < TAMANO_TABLERO and 0 <= y < TAMANO_TABLERO

def distancia_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

#                                                                        Funciones de movimiento del gato y el ratón usando algoritmo minimax
def movimiento_gato(tablero, gato, raton, max_movimientos):
    mejor_valor = float('inf')
    mejor_movimiento = gato

    for mov in movimientos:
        nuevo_x, nuevo_y = gato[0] + mov[0], gato[1] + mov[1]
        if es_posicion_valida(nuevo_x, nuevo_y):
            nuevo_gato = (nuevo_x, nuevo_y)
            if nuevo_gato == raton:
                return nuevo_gato
            if nuevo_gato == madriguera_raton:  # Evita que el gato entre en la madriguera
                continue
            valor = minimax(tablero, nuevo_gato, raton, 0, False, max_movimientos)
            heuristica = distancia_manhattan(nuevo_gato, raton)
            if valor + heuristica < mejor_valor:
                mejor_valor = valor + heuristica
                mejor_movimiento = nuevo_gato

    return mejor_movimiento

def movimiento_raton(tablero, gato, raton, max_movimientos):
    mejor_valor = -float('inf')
    mejor_movimiento = raton

    for mov in movimientos:
        nuevo_x, nuevo_y = raton[0] + mov[0], raton[1] + mov[1]
        if es_posicion_valida(nuevo_x, nuevo_y):
            nuevo_raton = (nuevo_x, nuevo_y)
            valor = minimax(tablero, gato, nuevo_raton, 0, True, max_movimientos)
            heuristica = distancia_manhattan(nuevo_raton, madriguera_raton)
            if valor - heuristica > mejor_valor:
                mejor_valor = valor - heuristica
                mejor_movimiento = nuevo_raton

    return mejor_movimiento

def minimax(tablero, gato, raton, profundidad, es_maximizador, max_movimientos):
    if gato == raton:
        return -10 + profundidad if es_maximizador else 10 - profundidad
    if raton == madriguera_raton:
        return 20 - profundidad if es_maximizador else -20 + profundidad
    if profundidad >= max_movimientos:
        return 0

    if es_maximizador:
        mejor_valor = -float('inf')
        for mov in movimientos:
            nuevo_x, nuevo_y = raton[0] + mov[0], raton[1] + mov[1]
            if es_posicion_valida(nuevo_x, nuevo_y):
                nuevo_raton = (nuevo_x, nuevo_y)
                valor = minimax(tablero, gato, nuevo_raton, profundidad + 1, False, max_movimientos)
                mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:
        peor_valor = float('inf')
        for mov in movimientos:
            nuevo_x, nuevo_y = gato[0] + mov[0], gato[1] + mov[1]
            if es_posicion_valida(nuevo_x, nuevo_y):
                nuevo_gato = (nuevo_x, nuevo_y)
                if nuevo_gato == madriguera_raton:  # Evita que el gato entre en la madriguera
                    continue
                valor = minimax(tablero, nuevo_gato, raton, profundidad + 1, True, max_movimientos)
                peor_valor = min(peor_valor, valor)
        return peor_valor



# --------------> IMPRESIONES <---------------

#                                                                              Impresion del tablero despues de cada jugada

def imprimir_tablero(tablero, pos_gato, pos_raton, madriguera):
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            if (i, j) == pos_gato:
                print("G", end=" ")
            elif (i, j) == pos_raton:
                if pos_raton == madriguera:
                    print("M", end=" ")
                else:
                    print("R", end=" ")
            elif (i, j) == madriguera:
                print("M", end=" ")
            else:
                print("-", end=" ")
        print()


#                                                                                 Impresion de posiciones iniciales
print("Posición Inicial")
imprimir_tablero(tablero, pos_gato, pos_raton, madriguera_raton)
print()





#                                                                                    Simulación del juego
max_movimientos_por_jugador = 6
turno = 0
raton_gano = False
gato_gano = False

while turno < 2 * max_movimientos_por_jugador:
    jugador = "Ratón" if turno % 2 == 0 else "Gato"
    print(f"Turno {turno + 1} - {jugador}")

    if turno % 2 == 0:
        if turno // 2 < max_movimientos_por_jugador:
            pos_raton = movimiento_raton(tablero, pos_gato, pos_raton, max_movimientos_por_jugador)
            if pos_raton == madriguera_raton:
                raton_gano = True
                break
    else:
        if turno // 2 < max_movimientos_por_jugador:
            pos_gato = movimiento_gato(tablero, pos_gato, pos_raton, max_movimientos_por_jugador)
            if pos_gato == pos_raton:
                gato_gano = True
                break
    turno += 1

    #                                                                                   Imprime el tablero durante las jugadas
    if not (gato_gano or raton_gano):
        imprimir_tablero(tablero, pos_gato, pos_raton, madriguera_raton)




# --------------> IMPRESIONES DEL FINAL DEL JUEGO <---------------



#                                                                                   Muestra el resultado final y el tablero correspondiente
if gato_gano:
    tablero[pos_raton[0]][pos_raton[1]] = "G"  # Muestra solo al gato en la posición del ratón atrapado
    imprimir_tablero(tablero, pos_gato, pos_raton, madriguera_raton)
    print("El gato atrapó al ratón.")
elif raton_gano:
    tablero[pos_raton[0]][pos_raton[1]] = "M"  # Muestra la madriguera con el ratón dentro
    imprimir_tablero(tablero, pos_gato, pos_raton, madriguera_raton)
    print("El ratón llegó a la madriguera y escapó.")
else:
    print("Se acabaron los movimientos, el gato no pudo atrapar al ratón")
