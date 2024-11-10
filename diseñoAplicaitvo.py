import csv
from collections import defaultdict
import heapq
import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para cargar los datos de los aeropuertos
def cargar_datos_aeropuertos(archivo_aeropuertos):
    aeropuertos = {}
    with open(archivo_aeropuertos, newline='', encoding='utf-8') as csvfile:
        lector = csv.reader(csvfile)
        for fila in lector:
            codigo_aeropuerto = fila[4]  # Código IATA (columna 5)
            nombre_aeropuerto = fila[1]  # Nombre del aeropuerto
            aeropuertos[codigo_aeropuerto] = nombre_aeropuerto
    return aeropuertos

# Función para cargar los datos de rutas desde routes.csv
def cargar_datos_rutas(archivo_rutas):
    grafo = defaultdict(list)
    with open(archivo_rutas, newline='', encoding='utf-8') as csvfile:
        lector = csv.reader(csvfile)
        for fila in lector:
            if len(fila) < 6:
                continue
            
            origen = fila[2]  # Código IATA del aeropuerto de origen (columna 3)
            destino = fila[4]  # Código IATA del aeropuerto de destino (columna 5)
            tiempo = 60  # Tiempo estimado de vuelo en minutos 
            
            if origen and destino:
                grafo[origen].append((tiempo, destino))
                grafo[destino].append((tiempo, origen))
    
    return grafo

# Función para implementar el algoritmo de Dijkstra
def dijkstra(grafo, inicio, destino):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]
    camino = {}
    
    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        if nodo_actual == destino:
            ruta = []
            while nodo_actual in camino:
                ruta.append(nodo_actual)
                nodo_actual = camino[nodo_actual]
            ruta.append(inicio)
            return distancia_actual, ruta[::-1]
        
        if distancia_actual > distancias[nodo_actual]:
            continue
        
        for tiempo, vecino in grafo[nodo_actual]:
            nueva_distancia = distancia_actual + tiempo
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                camino[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (nueva_distancia, vecino))
    
    return float('inf'), []

# Función para contar los cambios de aerolíneas
def contar_cambios(ruta):
    return len(ruta) - 2 if len(ruta) > 1 else 0

# Función para iniciar la búsqueda y mostrar los resultados
def buscar_ruta():
    origen = entrada_origen.get().upper()
    destino = entrada_destino.get().upper()
    
    if origen not in aeropuertos or destino not in aeropuertos:
        messagebox.showerror("Error", "Código de aeropuerto no válido o encontrado.")
        return
    
    distancia, ruta = dijkstra(grafo, origen, destino)
    if distancia == float('inf'):
        resultado.set(f"No hay ruta disponible de {origen} a {destino}")
    else:
        nombres_ruta = [aeropuertos[codigo] for codigo in ruta]
        cambios = contar_cambios(ruta)
        resultado.set(f"La ruta más rápida de {aeropuertos[origen]} a {aeropuertos[destino]} es:\n"
                      f"{' -> '.join(nombres_ruta)}\n"
                      f"Tiempo total: {distancia} minutos\n"
                      f"Con {cambios} cambio(s) de aerolínea")
        
        mostrar_grafo(ruta)

# Función para mostrar el grafo en la ventana
def mostrar_grafo(ruta):
    # Crear el grafo y añadir nodos y aristas
    G = nx.Graph()
    for i in range(len(ruta) - 1):
        G.add_edge(ruta[i], ruta[i + 1])
    
    # Dibujar el grafo
    fig, ax = plt.subplots(figsize=(5, 5))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1500, font_size=10, ax=ax)
    
    # Incrustar el gráfico en la ventana de Tkinter
    for widget in frame_grafo.winfo_children():
        widget.destroy()  # Limpiar el frame antes de dibujar el nuevo grafo
    canvas = FigureCanvasTkAgg(fig, master=frame_grafo)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Cargar los datos
archivo_aeropuertos = 'airports.csv'
archivo_rutas = 'routes.csv'
aeropuertos = cargar_datos_aeropuertos(archivo_aeropuertos)
grafo = cargar_datos_rutas(archivo_rutas)

# Interfaz gráfica con Tkinter
ventana = tk.Tk()
ventana.title("Búsqueda de Rutas entre Aeropuertos")
ventana.configure(bg='#e0f7fa')  # Color de fondo suave
fuente = ("Arial", 12)

# Campos de entrada
tk.Label(ventana, text="Aeropuerto de Origen (código):", bg='#e0f7fa', font=fuente).grid(row=0, column=0, padx=10, pady=10)
entrada_origen = tk.Entry(ventana, font=fuente)
entrada_origen.grid(row=0, column=1, padx=10, pady=10)

tk.Label(ventana, text="Aeropuerto de Destino (código):", bg='#e0f7fa', font=fuente).grid(row=1, column=0, padx=10, pady=10)
entrada_destino = tk.Entry(ventana, font=fuente)
entrada_destino.grid(row=1, column=1, padx=10, pady=10)

# Botón de búsqueda
boton_buscar = tk.Button(ventana, text="Buscar Ruta", command=buscar_ruta, bg='#4db6e4', fg='white', font=fuente)
boton_buscar.grid(row=2, columnspan=2, padx=10, pady=10)

# Mostrar resultado
resultado = tk.StringVar()
etiqueta_resultado = tk.Label(ventana, textvariable=resultado, justify="left", bg='#e0f7fa', font=fuente)
etiqueta_resultado.grid(row=3, columnspan=2, padx=10, pady=10)

# Frame para el grafo
frame_grafo = tk.Frame(ventana, bg='#e0f7fa')
frame_grafo.grid(row=4, columnspan=2, padx=10, pady=10)

ventana.mainloop()