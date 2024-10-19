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
        return False
    vertexCode = -1
    for i in codes:
        if codes[i] == code:
            vertexCode = codes[i]
        
    return [airport["Source Airport Code"],airport["Source Airport Name"],airport["Source Airport City"],airport["Source Airport Country"],airport["Source Airport Latitude"], airport["Source Airport Longitude"]], vertexCode


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

        print(f"Informacion del aeropuerto:\nCodigo: {airportData[0][0]}\nNombre: {airportData[0][1]}\nCiudad: {airportData[0][2]}\nPais: {airportData[0][3]}\nLatitud: {airportData[0][4]}\nLongitud: {airportData[0][5]}")

        # dijkstra
        
        op2 = input("¿Agregar otro aeropuerto para calcular el camino minimo?\n").upper().strip()
        if op2 == "SI":
            v2 = input("Ingrese codigo de aeropuerto: ").upper().strip()


