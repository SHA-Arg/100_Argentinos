# ordenamiento.py

def ordenar_respuestas(respuestas):
    """
    Ordena las respuestas ingresadas por puntos de mayor a menor usando el algoritmo de ordenamiento por inserción.

    Args:
    respuestas (list): Lista de tuplas donde cada tupla es (respuesta, puntos).

    Returns:
    list: Lista de tuplas ordenada por puntos de mayor a menor.
    """
    for i in range(1, len(respuestas)):
        cantidad_argdicen = respuestas[i]
        j = i - 1
        while j >= 0 and cantidad_argdicen[1] > respuestas[j][1]:
            respuestas[j + 1] = respuestas[j]
            j -= 1
        respuestas[j + 1] = cantidad_argdicen
    return respuestas


def ordenar_ranking(ranking):
    """
    Ordena el ranking de jugadores por puntaje de mayor a menor usando el algoritmo de ordenamiento por selección.

    Args:
    ranking (list): Lista de tuplas donde cada tupla es (nombre, puntaje).

    Returns:
    list: Lista de tuplas ordenada por puntaje de mayor a menor.
    """
    for i in range(len(ranking)):
        max_index = i
        for j in range(i + 1, len(ranking)):
            if ranking[j][1] > ranking[max_index][1]:
                max_index = j
        ranking[i], ranking[max_index] = ranking[max_index], ranking[i]
    return ranking
