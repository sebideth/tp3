class Coord:
    """
    Representa las coordenadas de una celda en una grilla 2D, representada
    como filas y columnas. Las coordendas ``fila = 0, columna = 0`` corresponden
    a la celda de arriba a la izquierda.

    Las instancias de Coord son inmutables.
    """

    def __init__(self, fila=0, columna=0):
        """Constructor.

        Argumentos:
            fila, columna (int): Coordenadas de la celda
        """
        raise NotImplementedError()

    def trasladar(self, df, dc):
        """Trasladar una celda.

        Devuelve una nueva instancia de Coord, correspondiente a las coordenadas
        de la celda que se encuentra ``df`` filas y ``dc`` columnas de distancia.

        Argumentos:
            df (int): Cantidad de filas a trasladar
            dc (int): Cantidad de columnas a trasladar

        Devuelve:
            Coord: Las coordenadas de la celda trasladada
        """
        raise NotImplementedError()

    def distancia(self, otra):
        """Distancia entre dos celdas.

        Argumentos:
            otra (Coord)

        Devuelve:
            int|float: La distancia entre las dos celdas (no negativo)
        """
        raise NotImplementedError()

    def __eq__(self, otra):
        """Determina si dos coordenadas son iguales"""
        raise NotImplementedError()

    def __iter__(self):
        """Iterar las componentes de la coordenada.

        Devuelve un iterador de forma tal que:
        >>> coord = Coord(3, 5)
        >>> f, c = coord
        >>> assert f == 3
        >>> assert c == 5
        """
        raise NotImplementedError()

    def __hash__(self):
        """Código "hash" de la instancia inmutable."""
        # Este método es llamado por la función de Python hash(objeto), y debe devolver
        # un número entero.
        # Más información (y un ejemplo de cómo implementar la funcion) en:
        # https://docs.python.org/3/reference/datamodel.html#object.__hash__
        raise NotImplementedError()

    def __repr__(self):
        """Representación de la coordenada como cadena de texto"""
        raise NotImplementedError()

class Mapa:
    """
    Representa el mapa de un laberinto en una grilla 2D con:

    * un tamaño determinado (filas y columnas)
    * una celda origen
    * una celda destino
    * 0 o más celdas "bloqueadas", que representan las paredes del laberinto

    Las instancias de Mapa son mutables.
    """
    def __init__(self, filas, columnas):
        """Constructor.

        El mapa creado tiene todas las celdas desbloqueadas, el origen en la celda
        de arriba a la izquierda y el destino en el extremo opuesto.

        Argumentos:
            filas, columnas (int): Tamaño del mapa
        """
        raise NotImplementedError()

    def dimension(self):
        """Dimensiones del mapa (filas y columnas).

        Devuelve:
            (int, int): Cantidad de filas y columnas
        """
        raise NotImplementedError()

    def origen(self):
        """Celda origen.

        Devuelve:
            Coord: Las coordenadas de la celda origen
        """
        raise NotImplementedError()

    def destino(self):
        """Celda destino.

        Devuelve:
            Coord: Las coordenadas de la celda destino
        """
        raise NotImplementedError()

    def asignar_origen(self, coord):
        """Asignar la celda origen.

        Argumentos:
            coord (Coord): Coordenadas de la celda origen
        """
        raise NotImplementedError()

    def asignar_destino(self, coord):
        """Asignar la celda destino.

        Argumentos:
            coord (Coord): Coordenadas de la celda destino
        """
        raise NotImplementedError()

    def celda_bloqueada(self, coord):
        """¿La celda está bloqueada?

        Argumentos:
            coord (Coord): Coordenadas de la celda

        Devuelve:
            bool: True si la celda está bloqueada
        """
        raise NotImplementedError()

    def bloquear(self, coord):
        """Bloquear una celda.

        Si la celda estaba previamente bloqueada, no hace nada.

        Argumentos:
            coord (Coord): Coordenadas de la celda a bloquear
        """
        raise NotImplementedError()

    def desbloquear(self, coord):
        """Desbloquear una celda.

        Si la celda estaba previamente desbloqueada, no hace nada.

        Argumentos:
            coord (Coord): Coordenadas de la celda a desbloquear
        """
        raise NotImplementedError()

    def alternar_bloque(self, coord):
        """Alternar entre celda bloqueada y desbloqueada.

        Si la celda estaba previamente desbloqueada, la bloquea, y viceversa.

        Argumentos:
            coord (Coord): Coordenadas de la celda a alternar
        """
        raise NotImplementedError()

    def es_coord_valida(self, coord):
        """¿Las coordenadas están dentro del mapa?

        Argumentos:
            coord (Coord): Coordenadas de una celda

        Devuelve:
            bool: True si las coordenadas corresponden a una celda dentro del mapa
        """
        raise NotImplementedError()

    def trasladar_coord(self, coord, df, dc):
        """Trasladar una coordenada, si es posible.

        Argumentos:
            coord: La coordenada de una celda en el mapa
            df, dc: La traslación a realizar

        Devuelve:
            Coord: La coordenada trasladada si queda dentro del mapa. En caso
                   contrario, devuelve la coordenada recibida.
        """
        raise NotImplementedError()

    def __iter__(self):
        """Iterar por las coordenadas de todas las celdas del mapa.

        Se debe garantizar que la iteración cubre todas las celdas del mapa, en
        cualquier orden.

        Ejemplo:
            >>> mapa = Mapa(10, 10)
            >>> for coord in mapa:
            >>>     print(coord, mapa.celda_bloqueada(coord))
        """
        raise NotImplementedError()
