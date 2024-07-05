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
