import customtkinter as ctk
import tkinter as tk
import time
#importar clases y constantes del motor logico
from Motor_Logico import MotorMapa, LIBRE, INICIO, FIN, OBJETO, CAMINO_TRAZADO
from Navegador_Algoritmico import BuscadorRutas

#paleta de colores minimalista y fria
colores = {
    LIBRE: "#1e1e1e",       # gris oscuro 
    OBJETO: "#555555",      # gris solido 
    INICIO: "#00bfff",      # azul brillante 
    FIN: "#dc143c",         # rojo carmesi
    CAMINO_TRAZADO: "#ffd700", # dorado para la ruta optima
    "grilla": "#2a2a2a"     # lineas separadoras tenues
}

class VisorRutas:
    def __init__(self, motor, buscador):
        self.motor = motor
        self.buscador = buscador
        
        #herramienta inicial por defecto
        self.herramienta_actual = OBJETO 

        #configuracion de la ventana
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.ventana = ctk.CTk()
        self.ventana.title("Motor de generador de Rutas")
        self.ventana.geometry("950x650")
        
        #tamano de cada cuadro en pixeles
        self.tamano_celda = 25
        
        self.construir_ui()
        self.dibujar_cuadricula()

    def construir_ui(self):
        #panel izquierdo para controles
        self.frame_controles = ctk.CTkFrame(self.ventana, width=200, corner_radius=10)
        self.frame_controles.pack(side="left", fill="y", padx=15, pady=15)
        
        #titulo de panel
        label_titulo = ctk.CTkLabel(self.frame_controles, text="herramientas", font=("arial", 16, "bold"))
        label_titulo.pack(pady=(20, 10))

        #instanciar botones de seleccion
        self.crear_boton_herramienta("Colocar inicio", INICIO, "#007acc")
        self.crear_boton_herramienta("Colocar fin", FIN, "#a3152d")
        self.crear_boton_herramienta("Dibujar muro", OBJETO, "#444444")
        self.crear_boton_herramienta("Borrador", LIBRE, "#333333")
        
        #separador visual
        ctk.CTkLabel(self.frame_controles, text="-"*30).pack(pady=10)
        
        #botones de accion principal
        btn_ejecutar = ctk.CTkButton(self.frame_controles, text="Ejecutar a*", 
                                     fg_color="#28a745", hover_color="#218838",
                                     command=self.iniciar_busqueda)
        btn_ejecutar.pack(pady=10, fill="x", padx=20)
        
        btn_limpiar = ctk.CTkButton(self.frame_controles, text="Limpiar mapa", 
                                    fg_color="#d9534f", hover_color="#c9302c",
                                    command=self.limpiar_todo)
        btn_limpiar.pack(pady=10, fill="x", padx=20)
        
        btn_generar_lab = ctk.CTkButton(self.frame_controles, text="Generar laberinto dfs", 
                                        fg_color="#8a2be2", hover_color="#5a189a",
                                        command=self.ejecutar_generador_dfs)
        btn_generar_lab.pack(pady=10, fill="x", padx=20)
        
        #separador visual para metricas
        ctk.CTkLabel(self.frame_controles, text="-"*30).pack(pady=10)
        
        #etiqueta de alto rendimiento para mostrar el tiempo
        self.label_tiempo = ctk.CTkLabel(self.frame_controles, text="tiempo de ejecucion: 0.000 ms", 
                                         font=("arial", 12), text_color="#00bfff")
        self.label_tiempo.pack(pady=5)

        #panel derecho para el mapa
        self.frame_mapa = ctk.CTkFrame(self.ventana, corner_radius=10)
        self.frame_mapa.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)
        
        ancho_canvas = self.motor.ancho_x * self.tamano_celda
        alto_canvas = self.motor.alto_y * self.tamano_celda
        
        #lienzo de rendimiento nativo
        self.canvas = tk.Canvas(self.frame_mapa, width=ancho_canvas, height=alto_canvas, 
                                bg=colores[LIBRE], highlightthickness=0)
        self.canvas.pack(padx=20, pady=20, anchor="center")
        
        #escaner de raton para clics y arrastre
        self.canvas.bind("<Button-1>", self.manejar_clic)
        self.canvas.bind("<B1-Motion>", self.manejar_clic)

    def crear_boton_herramienta(self, texto, valor_herramienta, color):
        #metodo auxiliar para no repetir codigo
        btn = ctk.CTkButton(self.frame_controles, text=texto, fg_color=color,
                            command=lambda: self.seleccionar_herramienta(valor_herramienta))
        btn.pack(pady=5, fill="x", padx=20)

    def seleccionar_herramienta(self, nueva_herramienta):
        self.herramienta_actual = nueva_herramienta

    def manejar_clic(self, evento):
        #calculo de coordenadas en base a pixeles
        columna_x = evento.x // self.tamano_celda
        fila_y = evento.y // self.tamano_celda
        
        #validacion estricta delegada al motor
        si_es_valido = self.motor.modificar_celda(columna_x, fila_y, self.herramienta_actual)
        if si_es_valido:
            # barrido de rutas previas al alterar el mapa
            self.motor.limpiar_solo_rutas() 
            self.dibujar_cuadricula()

    def dibujar_cuadricula(self):
        #purga total del lienzo
        self.canvas.delete("all")
        
        for y in range(self.motor.alto_y):
            for x in range(self.motor.ancho_x):
                valor_celda = self.motor.matriz[y][x]
                color = colores.get(valor_celda, colores[LIBRE])
                
                #vertices del rectangulo
                x1 = x * self.tamano_celda
                y1 = y * self.tamano_celda
                x2 = x1 + self.tamano_celda
                y2 = y1 + self.tamano_celda
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=colores["grilla"])