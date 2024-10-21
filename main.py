from Graph import Graph
import pandas as pd
import time
import folium


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
    g.add_edge(codes[e["Source Airport Code"]], codes[e["Destination Airport Code"]], g.calcDistance(e["Source Airport Latitude"],e["Source Airport Longitude"],e["Destination Airport Latitude"],e["Destination Airport Longitude"]))
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
    op = input("\nSeleccione una opcion:\n    1. Determinar si el grafo generado es conexo.\n    2. Determinar el peso del árbol de expansión mínima.\n    3. Buscar aeropuerto.\n    4. Salir\n")
    try: op = int(op)
    except: continue

    if op == 1:
        g.connected_components()
    elif op == 2:
        print("Arbol de expansion minima del grafo:")
        g.kruskal_mst_all_components()
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
            airportData1 = searchAirport(v2)

            # Si no lo encuentra
            if not airportData1:
                print("Aeropuerto no encontrado")
                continue

            dis, pad = g.dijkstra(codes[v1])
            # Mensaje en caso de que no sean de la misma componente
            if dis[codes[v2]] == float('inf'):
                print(f"No hay un camino disponible desde {v1} hasta {v2}.")
            else:
                # Hace el camino usando los predecesores
                path = []
                current = codes[v2]
                while current is not None:
                    path.append(current)
                    current = pad[current]

                # Invertimos el camino
                path.reverse()

                # Muestra el camino y la distancia
                print(f"Camino mínimo desde {v1} hasta {v2}:")
                for vertex in path:
                    airport = searchAirport(searchAirportCode(vertex))
                    print(f"Codigo: {airport[0]}, Nombre: {airport[1]}, Ciudad: {airport[2]}, Pais: {airport[3]}, Latitud: {airport[4]}, Longitud: {airport[5]}")

                print(f"Distancia total: {dis[codes[v2]]} Km")
                
                # Graficar el camino mínimo
                m = folium.Map(location=[(airportData[4] + airportData1[4]) / 2, (airportData[5] + airportData1[5]) / 2], zoom_start=3)



                # Marca las rutas
                points = [(searchAirport(searchAirportCode(vertex))[4], searchAirport(searchAirportCode(vertex))[5]) for vertex in path]
                folium.PolyLine(points, color='orange', weight=2.5, opacity=1).add_to(m)

                # Agregar marcadores para los vértices intermedios
                for vertex in path:
                    airport = searchAirport(searchAirportCode(vertex))
                    folium.Marker(
                        location=[airport[4], airport[5]],
                    popup=f"Código:{airport[0]} \n Nombre:{airport[1]}\n Ciudad: {airport[2]}\n Pais: {airport[3]}\n Latitud: {airport[4]}\n Longitud: {airport[5]}",
                        icon=folium.Icon(color='gray')
                    ).add_to(m)
                # Marcamos el aeropuerto inicial
                folium.Marker(
                    location=[airportData[4], airportData[5]],
                    popup=f"Código:{airportData[0]} \n Nombre:{airportData[1]}\n Ciudad: {airportData[2]}\n Pais: {airportData[3]}\n Latitud: {airportData[4]}\n Longitud: {airportData[5]}",
                    icon=folium.Icon(color='blue')
                ).add_to(m)
                
                # Marcam el aeropuerto de final
                folium.Marker(
                    location=[airportData1[4], airportData1[5]],
                    popup=f"Código:{airportData1[0]} \n Nombre:{airportData1[1]}\n Ciudad: {airportData1[2]}\n Pais: {airportData1[3]}\n Latitud: {airportData1[4]}\n Longitud: {airportData1[5]}",
                    icon=folium.Icon(color='green')
                ).add_to(m)

                # Guarda el mapa en un archivo HTML
                m.save("Map.html")
                print("Mapa guardado como Map.html")
            


