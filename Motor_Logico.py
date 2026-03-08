import numpy as np

#variables globales
LIBRE = 0
INICIO = 1
FIN = 2
OBJETO = 3
CAMINO_TRAZADO = 4
NODO_EXPLORADO = 5

class MotorMapa:
    def __init__(self, ancho_x, alto_y):
        # dimension del mapa
        self.ancho_x = ancho_x
        self.alto_y = alto_y
        # matriz optimizada, memoria gestionada por C
        self.matriz = np.zeros((alto_y, ancho_x), dtype=int)
        self.coordenada_inicio = None
        self.coordenada_fin = None

    def celda_valida(self, x, y):
        # validar limite
        return x >= 0 and x < self.ancho_x and y >= 0 and y < self.alto_y
    
    def modificar_celda(self, x, y, nuevo_tipo):
        if not self.celda_valida(x, y):
            return False
        tipo_actual = self.matriz[y][x]
        
        # solo un inicion y un fin
        if nuevo_tipo == INICIO:
            if self.coordenada_inicio != None:
                x_vieja, y_vieja = self.coordenada_inicio
                self.matriz[y_vieja][x_vieja] = LIBRE # borrar el viejo
            self.coordenada_inicio = (x, y) # guardar el nuevo
        
        if nuevo_tipo == FIN:
            if self.coordenada_fin != None:
                x_vieja, y_vieja = self.coordenada_fin
                self.matriz[y_vieja][x_vieja] = LIBRE # borrar el viejo
            self.coordenada_fin = (x, y) # guardar el nuevo
        
        # si se sobreescribe el inicio o fin
        if tipo_actual == INICIO and nuevo_tipo != INICIO:
            self.coordenada_inicio = None
        
        if tipo_actual == FIN and nuevo_tipo != FIN:
            self.coordenada_fin = None
        
        self.matriz[y][x] = nuevo_tipo
        return True
    
    def obtener_vecinos_caminables(self, x, y):
        # verificar donde saltar desde cada posicion
        vecinos_validos = []
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in movimientos:
            nuevo_x = x + dx
            nuevo_y = y + dy
            
            if self.celda_valida(nuevo_x, nuevo_y):
                if self.matriz[nuevo_y][nuevo_x] != OBJETO:
                    vecinos_validos.append((nuevo_x, nuevo_y))
        return vecinos_validos
    
    # motor de limpieza
    def limpiar_solo_rutas(self):
        for y in range(self.alto_y):
            for x in range(self.ancho_x):
                celda = self.matriz[y][x]
                if celda == CAMINO_TRAZADO or celda == NODO_EXPLORADO:
                    self.matriz[y][x] = LIBRE
    
    def limpiar_todo_el_mapa(self):
        self.matriz = np.zeros((self.alto_y, self.ancho_x), dtype=int)
        self.coordenada_inicio = None
        self.coordenada_fin = None