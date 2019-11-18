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
    for coord in mapa:
        mapa.bloquear(coord)
    mapa.asignar_origen(Coord(1,1))
    #Para que la celda destino tenga coordenadas impares
    if filas % 2 == 0:
        filas -= 1
    if columnas % 2 == 0:
        columnas -= 1
    mapa.asignar_destino(Coord(filas - 2, columnas - 2))
    visitadas = set()
    backtrack(mapa.origen(), visitadas, mapa)
    return mapa

def backtrack(celda, visitadas, mapa):
    '''Recursivamente va desbloqueando las celdas intermedias hasta que la lista de celdas
    vecinas queda vacia (condicion base) o termino de recorrer el mapa.
    '''
    visitadas.add(celda)
    mapa.paredes.remove(celda)
    celdas_vecinas = buscar_celdas_vecinas(celda, mapa, visitadas)
    while celdas_vecinas != []:
        vecina, intermedia = definir_celda_vecina_intermedia(celda, celdas_vecinas, mapa)
        visitadas.add(intermedia)
        mapa.paredes.remove(intermedia)
        backtrack(vecina, visitadas, mapa)
        celdas_vecinas = buscar_celdas_vecinas(celda, mapa, visitadas)

def buscar_celdas_vecinas(celda, mapa, visitadas):
    '''Crea la lista de las celdas vecinas posibles trasladando la coordenada actual en todas
    las direcciones posibles guardadas.
    '''
    posibles_direcciones_vecinas = [(2,0),(-2,0),(0,2),(0,-2)]
    celdas_vecinas = []
    for df, dc in posibles_direcciones_vecinas:
        vecina = mapa.trasladar_coord(celda, df, dc)
        if  vecina != celda and vecina not in visitadas:
            celdas_vecinas.append((df ,dc))
    return celdas_vecinas

def definir_celda_vecina_intermedia(celda, celdas_vecinas, mapa):
    '''Elije de manera aleatoria entre las posibles direcciones de las celdas vecinas
    y devuelve una tupla con la vecina elegida y la intermedia entre ella y la actual.
    '''
    direccion = choice(celdas_vecinas)
    vecina =  mapa.trasladar_coord(celda, direccion[0], direccion[1])
    intermedia =  mapa.trasladar_coord(celda, direccion[0] // 2, direccion[1] // 2)
    return vecina, intermedia
