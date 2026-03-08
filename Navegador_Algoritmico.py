import heapq
from Motor_Logico import LIBRE, OBJETO, INICIO, FIN
import random

class BuscadorRutas:
    def __init__(self,motor_mapa):
        self.motor = motor_mapa
        
    def distancia_manhattan(self,nodo_a,nodo_b):
        return abs(nodo_a[0] - nodo_b[0]) + abs(nodo_a[1] - nodo_b[1])
    
    #el algoritmo A*
    def ejecutar_a_estrella(self):
        inicio = self.motor.coordenada_inicio
        fin = self.motor.coordenada_fin
        
        #validacion de seguridad
        if inicio == None or fin == None:
            return False #no se puede buscar puntos sin definir
        
        #diccionario de memoria
        costo_g = {inicio: 0} # registra el costo para llegar a cada nodo
        padres = {inicio: None} # registra de que celda venimos
        
        #cola de prioridad
        cola_abierta = []
        heapq.heappush(cola_abierta, (0,inicio))
        
        while len(cola_abierta) > 0:
            #extraer el nodo menor
            _,actual = heapq.heappop(cola_abierta)
            
            #condicion de victoria
            if actual == fin:
                return self.reconstruir_camino(padres,fin)
            
            #usar radar del motor
            vecinos = self.motor.obtener_vecinos_caminables(actual[0],actual[1])
            
            for vecino in vecinos:
                #moverse a una celda libre cuesta 1
                nuevo_costo_g = costo_g[actual] + 1
                
                if vecino not in costo_g or  nuevo_costo_g < costo_g[vecino]:
                    #actualizar registros
                    costo_g[vecino] = nuevo_costo_g
                    padres[vecino] = actual
                    
                    #calcular prioridad total
                    costo_h = self.distancia_manhattan(vecino,fin)
                    costo_f = nuevo_costo_g + costo_h
                    
                    #meter a la cola para explorar despues
                    heapq.heappush(cola_abierta,(costo_f,vecino))
        #si se cerro el bucle estamos encerrados
        return False
    #metodo para construir ruta
    def reconstruir_camino(self,diccionario_padres, nodo_fin):
        camino = []
        actual = nodo_fin
        
        #viajar hacia atras
        while actual is not None:
            camino.append(actual)
            actual = diccionario_padres[actual]
        camino.reverse()
        return camino
    
    def generar_laberinto_dfs(self):
        #aislar el entorno, llenar todo de muros
        self.motor.limpiar_todo_el_mapa()
        for y in range(self.motor.alto_y):
            for x in range(self.motor.ancho_x):
                self.motor.matriz[y][x] = OBJETO

        #vectores de direccion (salto de 2 en 2 )
        #orden: arriba, derecha, abajo, izquierda
        dx_gen = [0, 2, 0, -2]
        dy_gen = [-2, 0, 2, 0]

        #funcion recursiva interna
        def excavar_recursivo(x, y):
            #cavar el camino en la posicion actual
            self.motor.matriz[y][x] = LIBRE
            
            #preparar y mezclar direcciones
            direcciones = [0, 1, 2, 3]
            random.shuffle(direcciones)
            
            #explorar cada direccion
            for i in range(4):
                dir_idx = direcciones[i]
                
                #nuevas coordenadas con salto de 2
                nx = x + dx_gen[dir_idx]
                ny = y + dy_gen[dir_idx]
                
                #validar que las nuevas coordenadas esten dentro de los limites absolutos
                if nx > 0 and nx < self.motor.ancho_x - 1 and ny > 0 and ny < self.motor.alto_y - 1:
                    if self.motor.matriz[ny][nx] == OBJETO:
                        #romper el muro intermedio
                        muro_x = x + (dx_gen[dir_idx] // 2)
                        muro_y = y + (dy_gen[dir_idx] // 2)
                        self.motor.matriz[muro_y][muro_x] = LIBRE
                        
                        #recursividad: viajar a la nueva posicion
                        excavar_recursivo(nx, ny)

        #iniciar en 1,1
        x_inicio, y_inicio = 1, 1
        excavar_recursivo(x_inicio, y_inicio)
        
        #establecer el inicio
        self.motor.modificar_celda(x_inicio, y_inicio, INICIO)

        #calcular la esquina opuesta para el fin
        x_fin = self.motor.ancho_x - 2 if self.motor.ancho_x % 2 != 0 else self.motor.ancho_x - 3
        y_fin = self.motor.alto_y - 2 if self.motor.alto_y % 2 != 0 else self.motor.alto_y - 3
        
        #forzamos la salida en esa posicion
        self.motor.matriz[y_fin][x_fin] = LIBRE
        self.motor.modificar_celda(x_fin, y_fin, FIN)