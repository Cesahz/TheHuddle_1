import heapq

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
            