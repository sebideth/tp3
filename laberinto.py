from mapa import Coord, Mapa
from random import choice
def generar_laberinto(filas, columnas):
    """Generar un laberinto.

    Argumentos:
        filas, columnas (int): Tamaño del mapa

    Devuelve:
        Mapa: un mapa nuevo con celdas bloqueadas formando un laberinto
              aleatorio
    """
    mapa = Mapa(filas, columnas)
    for i in range(0,filas):
        for j in range(0,columnas):
            mapa.bloquear(Coord(i,j))
    mapa.asignar_origen(Coord(1,1))
    mapa.asignar_destino(Coord(filas - 2, columnas - 2))

    visitadas = set()

    backtrack(mapa.origen(), visitadas, mapa)

    return mapa

def backtrack(celda, visitadas, mapa):
    visitadas.add(celda)
    mapa.paredes.remove(celda)
    celdas_vecinas = buscar_celdas_vecinas(celda, mapa, visitadas)
    if  celdas_vecinas == [] or celda == mapa.destino():
        return
    vecina, intermedia = definir_celda_vecina_intermedia(celda, celdas_vecinas, mapa)
    visitadas.add(intermedia)
    mapa.paredes.remove(intermedia)
    backtrack(vecina, visitadas, mapa)

def buscar_celdas_vecinas(celda, mapa, visitadas):
    posibles_celdas_vecinas = [(2,0),(-2,0),(0,2),(0,-2)]
    celdas_vecinas = []
    for df, dc in posibles_celdas_vecinas:
        vecina = mapa.trasladar_coord(celda, df, dc)
        if  vecina != celda and vecina not in visitadas:
            celdas_vecinas.append((df ,dc))
    return celdas_vecinas

def definir_celda_vecina_intermedia(celda, celdas_vecinas, mapa):
    dist = choice(celdas_vecinas)
    vecina =  mapa.trasladar_coord(celda, dist[0], dist[1])
    intermedia =  mapa.trasladar_coord(celda, dist[0] // 2, dist[1] // 2)
    return vecina, intermedia
