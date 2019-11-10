import tkinter as tk

from mapa import Coord, Mapa
from laberinto import generar_laberinto
from ia import IA

DISTANCIA_NIEBLA = 2

class Color:
    VACIO = 'white'
    BLOQUE = 'black'
    ORIGEN = 'red'
    DESTINO = 'green'
    NIEBLA = 'gray'
    VISITADO = 'cyan'
    CAMINO = 'blue'
    JUGADOR = 'yellow'

    @staticmethod
    def basico(mapa, coord):
        if coord == mapa.origen():
            return Color.ORIGEN
        if coord == mapa.destino():
            return Color.DESTINO
        if mapa.celda_bloqueada(coord):
            return Color.BLOQUE
        return Color.VACIO

    @staticmethod
    def con_niebla(mapa, coord, coord_jugador):
        if coord == coord_jugador:
            return Color.JUGADOR
        if coord_jugador.distancia(coord) > DISTANCIA_NIEBLA:
            return Color.NIEBLA
        return Color.basico(mapa, coord)

    @staticmethod
    def backtracking(mapa, coord, coord_jugador, visitados, camino):
        if coord == coord_jugador:
            return Color.JUGADOR
        if coord in camino:
            return Color.CAMINO
        if coord in visitados:
            return Color.VISITADO
        return Color.basico(mapa, coord)

class Vista(tk.Canvas):
    TAM_CELDA_PX = 20

    def __init__(self, contenedor, mapa):
        filas, columnas = mapa.dimension()
        super().__init__(contenedor, width=columnas * Vista.TAM_CELDA_PX, height=filas * Vista.TAM_CELDA_PX)
        self.mapa = mapa

    def actualizar(self, obtener_color_celda):
        self.delete("all")
        for coord in self.mapa:
            color = obtener_color_celda(self.mapa, coord)
            f, c = coord
            x = c * Vista.TAM_CELDA_PX
            y = f * Vista.TAM_CELDA_PX
            self.create_rectangle((x, y, x + Vista.TAM_CELDA_PX, y + Vista.TAM_CELDA_PX), fill=color, outline="")

    def coord_px_a_celda(self, x, y):
        return Coord(int(y // Vista.TAM_CELDA_PX), int(x // Vista.TAM_CELDA_PX))

class Editor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.modo = None

        self.title("TP3 - Editor")
        self.resizable(False, False)

        self.filas = tk.IntVar()
        self.filas.set(21)

        self.columnas = tk.IntVar()
        self.columnas.set(31)

        self.mapa = self.crear_mapa()

        self.modo_arrastre = False

        panel = tk.Frame(self)
        panel.grid(column=0, row=0, sticky="nwes", padx=5, pady=5)

        dimension = tk.Frame(panel)
        dimension.grid(row=0, sticky="nwes")

        tk.Label(dimension, text="Filas").grid(row=0, column=0, padx=(0, 5), sticky="e")
        tk.Spinbox(dimension, textvariable=self.filas, from_=5, to=1000, width=5).grid(row=0, column=1, sticky="w")

        tk.Label(dimension, text="Columnas").grid(row=1, column=0, padx=(0, 5), sticky="e")
        tk.Spinbox(dimension, textvariable=self.columnas, from_=5, to=1000, width=5).grid(row=1, column=1, sticky="w")

        self.filas.trace('w', self.cambiar_dimension)
        self.columnas.trace('w', self.cambiar_dimension)

        tk.Button(panel, text="Generar", command=self.generar).grid(row=1, sticky="we", pady=5)

        panel.rowconfigure(2, weight=1)

        tk.Button(panel, text="Jugar", command=self.jugar).grid(row=3, sticky="we")
        tk.Button(panel, text="IA", command=self.ia).grid(row=4, sticky="we", pady=(5, 0))

        self.vista = self.crear_vista()

        self.actualizar_vista()

    def cambiar_dimension(self, *args):
        self.reemplazar_mapa(self.crear_mapa())

    def crear_mapa(self):
        try:
            return Mapa(self.filas.get(), self.columnas.get())
        except tk.TclError:
            return self.mapa

    def crear_vista(self):
        vista = Vista(self, self.mapa)
        vista.grid(column=1, row=0, sticky="nwes", padx=5, pady=5)

        vista.bind("<1>", lambda e: self.alternar_bloque(self.vista.coord_px_a_celda(e.x, e.y)))
        vista.bind("<2>", lambda e: self.asignar_origen(self.vista.coord_px_a_celda(e.x, e.y)))
        vista.bind("<3>", lambda e: self.asignar_destino(self.vista.coord_px_a_celda(e.x, e.y)))
        vista.bind("<B1-Motion>", lambda e: self.arrastrar(self.vista.coord_px_a_celda(e.x, e.y)))

        return vista

    def actualizar_vista(self):
        self.vista.actualizar(Color.basico)

    def alternar_bloque(self, coord):
        self.mapa.alternar_bloque(coord)
        self.modo_arrastre = self.mapa.celda_bloqueada(coord)
        self.actualizar_vista()

    def arrastrar(self, coord):
        if self.modo_arrastre:
           self.mapa.bloquear(coord)
        else:
           self.mapa.desbloquear(coord)
        self.actualizar_vista()

    def asignar_origen(self, coord):
        self.mapa.asignar_origen(coord)
        self.actualizar_vista()

    def asignar_destino(self, coord):
        self.mapa.asignar_destino(coord)
        self.actualizar_vista()

    def generar(self):
        self.reemplazar_mapa(generar_laberinto(self.filas.get(), self.columnas.get()))

    def reemplazar_mapa(self, mapa):
        self.mapa = mapa
        self.vista.grid_forget()
        self.vista.destroy()
        self.vista = self.crear_vista()
        self.actualizar_vista()

    def jugar(self):
        self.ir_a_modo(ModoJuego(self))

    def ia(self):
        self.ir_a_modo(ModoIA(self))

    def ir_a_modo(self, modo):
        self.modo = modo
        self.modo.protocol("WM_DELETE_WINDOW", lambda: self.modo_terminado())
        self.modo.bind("<Destroy>", lambda e: self.modo_terminado())
        self.withdraw()

    def modo_terminado(self):
        if self.modo:
            self.modo.destroy()
            self.modo = None
        self.deiconify()

class ModoJuego(tk.Toplevel):
    def __init__(self, editor):
        super().__init__(editor)

        self.resizable(False, False)

        self.title("TP3 - Jugador")

        self.vista = Vista(self, editor.mapa)
        self.vista.grid()

        self.mapa = editor.mapa
        self.coord_jugador = self.mapa.origen()

        self.bind('<Left>', lambda e: self.mover(0, -1))
        self.bind('<Right>', lambda e: self.mover(0, 1))
        self.bind('<Up>', lambda e: self.mover(-1, 0))
        self.bind('<Down>', lambda e: self.mover(1, 0))

        self.bind('<Escape>', lambda e: self.destroy())

        self.actualizar_vista()

    def mover(self, df, dc):
        coord_nueva = self.mapa.trasladar_coord(self.coord_jugador, df, dc)
        if self.mapa.celda_bloqueada(coord_nueva):
            return
        self.coord_jugador = coord_nueva
        self.actualizar_vista()

    def actualizar_vista(self):
        self.vista.actualizar(self.obtener_color_celda)

    def obtener_color_celda(self, mapa, coord):
        return Color.con_niebla(mapa, coord, self.coord_jugador)

class ModoIA(tk.Toplevel):
    def __init__(self, editor):
        super().__init__(editor)

        self.resizable(False, False)

        self.title("TP3 - Backtracking")

        self.vista = Vista(self, editor.mapa)
        self.vista.grid()

        self.ia = IA(editor.mapa)

        self.bind('<Escape>', lambda e: self.destroy())

        self.actualizar_vista()
        self.esperar_y_avanzar()

    def esperar_y_avanzar(self):
        self.after(50, self.avanzar)

    def avanzar(self):
        self.ia.avanzar()
        self.actualizar_vista()
        self.esperar_y_avanzar()

    def actualizar_vista(self):
        coord_jugador = self.ia.coord_jugador()
        visitados = set(self.ia.visitados())
        camino = set(self.ia.camino())

        def obtener_color_celda(mapa, coord):
            return Color.backtracking(mapa, coord, coord_jugador, visitados, camino)

        self.vista.actualizar(obtener_color_celda)

def main():
    Editor().mainloop()

main()
