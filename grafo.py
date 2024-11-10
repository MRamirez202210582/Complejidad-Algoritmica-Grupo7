# import networkx as nx
# import matplotlib.pyplot as plt

# def visualizar_grafo_aeropuertos(inicio, fin):
#     # Inicializa el diccionario para aeropuertos
#     airports = {}

#     # Lee el archivo de aeropuertos y limita a los nodos entre 
#     with open('airports.csv', newline='', encoding='utf-8') as f:
#         next(f)
#         count = 0
#         for line in f:
#             if count >= fin:
#                 break
#             if count < inicio:
#                 count += 1
#                 continue
#             data = line.strip().split(',')
#             airport_id = int(data[0])
#             name = data[1]
#             try:
#                 latitude = float(data[6])
#                 longitude = float(data[7])
#                 airports[airport_id] = {'name': name, 'pos': (longitude, latitude)}
#                 count += 1
#             except ValueError:
#                 continue

#     # Inicializa la lista de rutas
#     routes = []

#     # Leer el archivo de rutas
#     with open('routes.csv', newline='', encoding='utf-8') as f:
#         next(f)
#         for line in f:
#             data = line.strip().split(',')
#             try:
#                 source_id = int(data[3])
#                 dest_id = int(data[5])
#                 if source_id in airports and dest_id in airports:
#                     routes.append((source_id, dest_id))
#             except ValueError:
#                 continue

#     # Crear el grafo
#     G = nx.Graph()
#     for airport_id, attrs in airports.items():
#         if any(source_id == airport_id or dest_id == airport_id for source_id, dest_id in routes):
#             G.add_node(airport_id, **attrs)

#     G.add_edges_from(routes)

#     # Filtra los nodos conectados
#     connected_nodes = [n for n in G.nodes() if G.degree(n) > 0]
#     G_connected = G.subgraph(connected_nodes)

#     # Visualizar el grafo solo si hay nodos conectados
#     if len(G_connected.nodes()) > 0:
#         pos = nx.spring_layout(G_connected)
#         nx.draw(G_connected, pos, with_labels=True, labels=nx.get_node_attributes(G_connected, 'name'), node_size=50, font_size=8)

#         plt.title(f"Grafo de Aeropuertos (mostrando {len(G_connected.nodes())} nodos conectados)")
#         plt.show()

# # Ejemplo de uso de la función
# visualizar_grafo_aeropuertos(0, 500)
import networkx as nx
from pyvis.network import Network

def construir_grafo_aeropuertos():
    airports = {}

    # Lee el archivo de aeropuertos y limita a 500 nodos
    with open('airports.csv', newline='', encoding='utf-8') as f:
        next(f)  # Saltar el encabezado
        count = 0
        for line in f:
            if count >= 500:
                break
            data = line.strip().split(',')
            airport_id = int(data[0])
            name = data[1]
            try:
                latitude = float(data[6])
                longitude = float(data[7])
                airports[airport_id] = {'name': name, 'pos': (longitude, latitude)}
                count += 1
            except ValueError:
                continue

    routes = []

    # Leer el archivo de rutas
    with open('routes.csv', newline='', encoding='utf-8') as f:
        next(f)  # Saltar el encabezado
        for line in f:
            data = line.strip().split(',')
            try:
                source_id = int(data[3])
                dest_id = int(data[5])
                if source_id in airports and dest_id in airports:
                    routes.append((source_id, dest_id))
            except ValueError:
                continue

    # Crear el grafo
    G = nx.Graph()
    
    # Agregar nodos y filtrar solo los que tienen conexiones
    G.add_edges_from(routes)

    # Filtrar nodos que tienen al menos una conexión
    connected_nodes = [n for n in G.nodes() if G.degree(n) > 0]
    G_connected = G.subgraph(connected_nodes)

    return G_connected, airports

def visualizar_grafo_html(grafo, airports):
    net = Network(notebook=False)

    for airport_id, attrs in airports.items():
        if airport_id in grafo.nodes():  # Solo agregar nodos que están conectados
            net.add_node(airport_id, label=attrs['name'])

    net.add_edges(grafo.edges)

    # Generar el archivo HTML
    net.write_html("grafo_aeropuertos.html")

# Construir y visualizar el grafo
grafo_aeropuertos, aeropuertos = construir_grafo_aeropuertos()
visualizar_grafo_html(grafo_aeropuertos, aeropuertos)