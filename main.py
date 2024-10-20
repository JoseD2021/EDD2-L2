from Graph import Graph
import pandas as pd
import time


inicio = time.time() #debug
# Carga de datos csv to graph
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
fin = time.time()
print(fin-inicio,"seg")

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

def searchAirportCode(vertex: int):
    vertexCode = False
    for i in codes:
        if codes[i] == vertex:
            vertexCode = i
    return vertexCode

#menu
op = -1
while op != 4:
    op = input("Seleccione una opcion:\n    1. Determinar si el grafo generado es conexo.\n    2. Determinar el peso del árbol de expansión mínima.\n    3. Buscar aeropuerto.\n    4. Salir\n")
    try: op = int(op)
    except: continue

    if op == 1:
        g.connected_components()
    elif op == 2:
        pass
    elif op == 3:
        v1 = input("Ingrese codigo de aeropuerto: ").upper().strip()
        airportData = searchAirport(v1)

        if not airportData:
            print("Aeropuerto no encontrado")
            continue

        print(f"Informacion del aeropuerto:\nCodigo: {airportData[0]}\nNombre: {airportData[1]}\nCiudad: {airportData[2]}\nPais: {airportData[3]}\nLatitud: {airportData[4]}\nLongitud: {airportData[5]}\n")
        print("Aeropuertos cuyos caminos minimos son mas largos:\n")
        longest = g.longestPaths(codes[v1])
        for i,path in enumerate(longest):
            newData = searchAirport(searchAirportCode(path[1]))
            print(f"{i+1}) Codigo: {newData[0]}, Nombre: {newData[1]}, Ciudad: {newData[2]}, Pais: {newData[3]}, Latitud: {newData[4]}, Longitud: {newData[5]}. Distancia: {path[0]}Km")
        
        op2 = input("¿Agregar otro aeropuerto para calcular el camino minimo?\n").upper().strip()
        if op2 == "SI":
            v2 = input("Ingrese codigo de aeropuerto: ").upper().strip()


