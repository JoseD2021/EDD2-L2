from Graph import Graph
import pandas as pd
import time

inicio = time.time()

df = pd.read_csv("flights_final.csv")



codes = {} # Registro clave = Int vertice, Valor = Airport Code
codesI = 0

for _,e in df.iterrows(): # recorre cada fila del csv
    if not e["Source Airport Code"] in codes:
        codes[e["Source Airport Code"]] = codesI
        codesI+=1
    if not e["Destination Airport Code"] in codes:
        codes[e["Destination Airport Code"]] = codesI
        codesI+=1

#g = Graph(len(codes))
#for _,e in df.iterrows(): # recorre cada fila del csv
#    # Agrega todas las aristas
#    g.add_edge(codes[e["Source Airport Code"]], codes[e["Destination Airport Code"]], g.calcDistance(e["Source Airport Longitude"],e["Source Airport Latitude"],e["Destination Airport Longitude"],e["Destination Airport Latitude"]))
#
def searchAirportCode(vertex: int):
    vertexCode = False
    for i in codes:
        if codes[i] == vertex:
            vertexCode = i
    return vertexCode
def searchAirport(code: str):
    try:
        airport = df[df["Source Airport Code"] == code].iloc[0]
    except:
        try: 
            airport = df[df["Destination Airport Code"] == code].iloc[0]
        except:
            return False
        return airport["Destination Airport Code"],airport["Destination Airport Name"],airport["Destination Airport City"],airport["Destination Airport Country"],airport["Destination Airport Latitude"], airport["Destination Airport Longitude"]
    return airport["Source Airport Code"],airport["Source Airport Name"],airport["Source Airport City"],airport["Source Airport Country"],airport["Source Airport Latitude"], airport["Source Airport Longitude"]

import folium
def todo():
    m = folium.Map()
    for vertex in codes:
        # print(vertex)
        airport = searchAirport(vertex)
        folium.Marker(
            location=[airport[4], airport[5]],
        popup=f"Código:{airport[0]} \n Nombre:{airport[1]}\n Ciudad: {airport[2]}\n Pais: {airport[3]}\n Latitud: {airport[4]}\n Longitud: {airport[5]}",
            icon=folium.Icon(color='gray')
        ).add_to(m)
    m.save("Map.html")
    print("Mapa guardado como Map.html")

# print(searchAirportCode(906))
# print(searchAirportCode(1270))
#for airport in df.iterrows():
#    print(airport[0])
#    break
todo()
#g.connected_components()
#print(g.dijkstra(120)[1])

#print(g.longestPath(0))
#print("=====================")
#print(g.longestPathX(0))

fin = time.time()
print(fin-inicio,"seg")