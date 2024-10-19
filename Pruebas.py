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

g = Graph(len(codes))
for _,e in df.iterrows(): # recorre cada fila del csv
    # Agrega todas las aristas
    g.add_edge(codes[e["Source Airport Code"]], codes[e["Destination Airport Code"]], g.calcDistance(e["Source Airport Longitude"],e["Source Airport Latitude"],e["Destination Airport Longitude"],e["Destination Airport Latitude"]))

def searchAirport(code: str):
    try:
        airport = df[df["Source Airport Code"] == code].iloc[0]
    except:
        return False
    vertexCode = -1
    for i in codes:
        if codes[i] == code:
            vertexCode = codes[i]
    
    return [airport["Source Airport Code"],airport["Source Airport Name"],airport["Source Airport City"],airport["Source Airport Country"],airport["Source Airport Latitude"], airport["Source Airport Longitude"]], vertexCode

print(g.dijkstra(0)[0])

fin = time.time()
print(fin-inicio,"seg")