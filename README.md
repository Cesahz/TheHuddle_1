# ⚙️Simulador de Entornos y Optimización de Rutas A\*

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![NumPy](https://img.shields.io/badge/NumPy-Optimized-success.svg)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-darkblue.svg)

## 📌 Visión General

**El simulador** es un motor lógico de cálculo de trayectorias y simulación procedural de entornos grid-based (cuadrículas). Diseñado con un enfoque estricto en la eficiencia de memoria y la velocidad de ejecución, el sistema implementa el algoritmo **A\*** para la resolución de rutas óptimas y un generador de laberintos mediante **Búsqueda en Profundidad (DFS)**.

El proyecto está construido bajo una arquitectura modular estricta, garantizando un entorno 100% controlado donde la lógica matemática opera de forma insonorizada y totalmente aislada de la capa de presentación visual.

## 🏗️ Arquitectura del Sistema (MVC)

El código respeta el principio de responsabilidad única, dividiendo el sistema en tres dominios absolutos:

1. **Motor Lógico (El Modelo):** - Utiliza `numpy` para gestionar una matriz bidimensional de enteros. Al delegar la memoria a C, se elimina la sobrecarga de comparar strings, garantizando operaciones instantáneas a gran escala.
   - Actúa como el juez absoluto del entorno, validando límites y previniendo superposiciones de entidades.

2. **Navegador Algorítmico (El Cerebro/Controlador):**
   - **A\* (A-Star):** Implementado con `heapq` (colas de prioridad) y heurística Manhattan. Calcula el camino más corto evaluando $f(n) = g(n) + h(n)$.
   - **Generador DFS:** Adaptación de un algoritmo _Recursive Backtracker_ de C++ a Python, optimizado con manipulación del `sys.setrecursionlimit` para tallar laberintos perfectos sin colapsos de memoria.

3. **Interfaz Visual (La Vista):**
   - Interfaz minimalista y asíncrona desarrollada con `customtkinter`.
   - Renderizado espacial de alta velocidad utilizando el `Canvas` nativo de Tkinter, capaz de repintar miles de celdas por segundo sin latencia.

## 🚀 Características Principales

- **Dibujo Espacial Dinámico:** Creación de muros inquebrantables, inicio y fin en tiempo real mediante eventos de ratón (arrastre continuo).
- **Adaptación Continua:** El sistema permite re-ejecutar algoritmos sobre el mismo mapa, limpiando rastros anteriores pero conservando la estructura de los obstáculos.
- **Métricas Clínicas:** Incorporación de un benchmark de alto rendimiento (`time.perf_counter`) que evalúa el tiempo de ejecución de la búsqueda matemática en milisegundos, demostrando la eficiencia del código subyacente.

## ⚙️ Instalación y Despliegue

Asegúrate de tener Python instalado en tu sistema.

1. Clona este repositorio:
   ```bash
   git clone [https://github.com/TU_USUARIO/motor-mahoraga.git](https://git@github.com:Cesahz/TheHuddle_1.git)
   ```
2. Instala la dependencia principal:
   ```bash
   pip install numpy customtkinter
   ```
3. Ejecuta el orquestador principal:
   ```bash
   python interfaz.py
   ```
