from mapa import Coord, Mapa

def generar_laberinto(filas, columnas):
    """Generar un laberinto.

    Argumentos:
        filas, columnas (int): Tamaño del mapa

    Devuelve:
        Mapa: un mapa nuevo con celdas bloqueadas formando un laberinto
              aleatorio
    """
    mapa = Mapa(filas, columnas)
    for i in range(columnas):
        mapa.bloquear(Coord(0, i))
        mapa.bloquear(Coord(filas - 1, i))
    for i in range(filas):
        mapa.bloquear(Coord(i, 0))
        mapa.bloquear(Coord(i, columnas - 1))

    mapa.asignar_origen(Coord(1,1))
    mapa.asignar_destino(Coord(filas - 2, columnas - 2))
    return mapa
