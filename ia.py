from mapa import *

class IA:
    """
    Inteligencia artificial para resolver un laberinto.

    Se simula un jugador que comienza en la celda de origen, y mediante
    el método avanzar() el jugador hace un movimiento.

    Ejemplo:
        >>> mapa = Mapa(10, 10)
        >>> ia = IA()
        >>> ia.coord_jugador()
        Coord(0, 0)
        >>> while ia.coord_jugador() != mapa.destino()
        ...     ia.avanzar()
        >>> ia.coord_jugador()
        Coord(9, 9)
    """

    def __init__(self, mapa):
        """Constructor.

        Argumentos:
            mapa (Mapa): El mapa con el laberinto a resolver
        """
        self.mapa = mapa
        self.actual = mapa.coord_origen
        self.visitadas = set()
        self.recorrido = []

    def coord_jugador(self):
        """Coordenadas del "jugador".

        Devuelve las coordenadas de la celda en la que se encuentra el jugador.

        Devuelve:
            Coord: Coordenadas del "jugador"

        Ejemplo:
            >>> ia = IA(Mapa(10, 10))
            >>> ia.coord_jugador()
            Coord(0, 0)
            >>> ia.avanzar()
            >>> ia.coord_jugador()
            Coord(1, 0)
            >>> ia.avanzar()
            >>> ia.coord_jugador()
            Coord(2, 0)
        """
        return self.actual

    def visitados(self):
        """Celdas visitadas.

        Devuelve:
            secuencia<Coord>: Devuelve la lista (o cualqueir otra secuencia) de
            de celdas visitadas al menos una vez por el jugador desde que
            comenzó la simulación.

        Ejemplo:
            >>> ia = IA(Mapa(10, 10))
            >>> ia.avanzar()
            >>> ia.avanzar()
            >>> ia.avanzar()
            >>> ia.visitados()
            [Coord(0, 0), Coord(1, 0),  Coord(2, 0)]
        """
        return self.visitadas

    def camino(self):
        """Camino principal calculado.

        Devuelve:
            secuencia<Coord>: Devuelve la lista (o cualqueir otra secuencia) de
            de celdas que componen el camino desde el origen hasta la posición
            del jugador. Esta lista debe ser un subconjunto de visitados().

        Ejemplo:
            >>> ia = IA(Mapa(10, 10))
            >>> for i in range(6):
            ...     ia.avanzar()
            >>> ia.visitados()
            [Coord(0, 0), Coord(1, 0), Coord(1, 1),  Coord(2, 0),  Coord(3, 0),  Coord(4, 0)]
            >>> ia.camino()
            [Coord(0, 0), Coord(1, 0),  Coord(2, 0),  Coord(3, 0),  Coord(4, 0)]

        Nota:
            La celda actual en la que está el jugador puede no estar en la
            lista devuelta (esto tal vez permite simplificar la
            implementación).
        """
        return self.recorrido

    def avanzar(self):
        """Avanza un paso en la simulación.

        Si el jugador no está en la celda destino, y hay algún movimiento
        posible hacia una celda no visitada, se efectúa ese movimiento.
        """
        if self.actual != self.mapa.origen(): #Para que la celda origen no quede pintada de celeste
            self.visitadas.add(self.actual)
        if self.actual == self.mapa.destino():
            return
        celdas_vecinas = buscar_celdas_vecinas(self.actual, self.mapa, self.visitadas)
        if celdas_vecinas != []:
            if self.actual != self.mapa.origen(): #Para que la celda origen no quede pintada de azul
                self.recorrido.append(self.actual)
            vecina = celdas_vecinas[0]
            self.recorrido.append(vecina)
            self.actual = vecina
        else:
            self.actual = self.recorrido.pop()

def buscar_celdas_vecinas(celda, mapa, visitadas):
    '''Dada una celda, mapa y un conjunto de celdas visitadas,
    devuelve una lista de todas las celdas vecinas válidas.'''
    posible_direcciones = [(1,0),(0,1),(-1,0),(0,-1)] #Abajo, Derecha, Arriba, Izquierda.Así llega más rápido al destino
    celdas_vecinas = []
    for df, dc in posible_direcciones:
        vecina = mapa.trasladar_coord(celda, df, dc)
        if  vecina != celda and vecina not in mapa.paredes and vecina not in visitadas:
            celdas_vecinas.append(vecina)
    return celdas_vecinas
