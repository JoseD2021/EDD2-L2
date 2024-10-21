from typing import List
import math

class DisjointSet:
    def __init__(self, n):
        # Inicializar el conjunto disjunto
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        # Encontrar la raíz del conjunto del nodo u
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # Compresión de caminos
        return self.parent[u]

    def union(self, u, v):
        # Unir los conjuntos de u y v usando unión por rango
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

class Graph:
    R = 6378 #6371 # Radio promedio de la tierra, 6378 radio ecuatorial
    def __init__ (self, n: int, directed: bool = False):
        self.n = n
        self.directed = directed
        self.L: List[List[int]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, weight: float = 1) -> bool:
        if 0 <= u < self.n and 0 <= v < self.n:
            self.L[u].append((v, weight)) # Guardar el peso
            if not self.directed:
                self.L[v].append((u, weight))
            return True
        return False


    def DFS(self, u: int) -> None:
        visit = [False for _ in range(self.n)]
        self.__DFS_visit(u, visit)
        print()

    # Calcular las componentes conexas y el número de vértices en cada una
    def connected_components(self):
        visit = [False] * self.n # Lista para marcar los nodos visitados
        components = [] # Lista de componentes, cada componente es una lista de vértices
        
        for u in range(self.n):
            if not visit[u]:
                # Realizar DFS para encontrar todos los nodos en la misma componente que u
                component = []
                self.__DFS_collect(u, visit, component)
                components.append(component)
        
        # Si hay solo una componente, el grafo es conexo
        if len(components) == 1:
            print("El grafo es conexo.")
        else:
            print(f"El grafo no es conexo. Tiene {len(components)} componentes.")
            for i, component in enumerate(components):
                print(f"Componente {i + 1} tiene {len(component)} vértices")#: {(component)}")
    
    # DFS modificado para recolectar todos los vértices de una componente
    def __DFS_collect(self, u: int, visit: List[bool], component: List[int]) -> None:
        visit[u] = True
        component.append(u)
        for v, _ in self.L[u]: # Recorrer solo los vecinos
            if not visit[v]:
                 self.__DFS_collect(v, visit, component)    

    def __DFS_visit(self, u: int, visit: List[bool], Print: bool = True) -> List:
        visit[u] = True
        if Print:
            print(u, end=' ')
        for v, _ in self.L[u]:    # Ajustar para tomar solo el vértice v
            if not visit[v]:
                visit = self.__DFS_visit(v, visit, Print)
        return visit

    def calcDistance(self,lat1,long1,lat2,long2): # Fórmula del Haversine
        lat1, long1, lat2, long2 = map(math.radians, [lat1, long1, lat2, long2])
        lat = lat2 - lat1
        long = long2 - long1
        a = math.sin(lat/2)**2 + math.cos(lat1)*math.cos(lat2)*(math.sin(long/2)**2)
        c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        d = self.R*c
        return d

    def dijkstra(self, v0):
        D = [float("inf")] * self.n
        pad = [None] * self.n
        visit = [None] * self.n
        D[v0] = 0

        while not all(visit):
            min_distance = float('inf')
            v = None
            for i in range(self.n):
                if not visit[i] and D[i] < min_distance:
                    min_distance = D[i]
                    v = i
            
            if v is None:
                break

            visit[v] = True

            for j in self.L[v]:
                i = j[0]
                if not visit[i]:
                    alt = D[v] + j[1]
                    if alt < D[i]:
                        D[i] = alt
                        pad[i] = v

        return D, pad

    
    def longestPaths(self,v):
        D, pad = self.dijkstra(v)
        maxPaths = []
        for index, distance in enumerate(D):
            if distance == float('inf') or distance == 0:  # descarta los valores infinito y el mismo aeropuerto
                continue
            if len(maxPaths) < 10:
                maxPaths.append((distance,index))
            else:   # si se reemplaza la menor distancia de la lista si se encuentra un valor mayor
                m = 0
                for j in range(len(maxPaths)):
                    if maxPaths[j][0] < maxPaths[m][0]:
                        m = j
                if distance > maxPaths[m][0]:
                    maxPaths[m] = (distance,index)
            
        maxPaths.sort(reverse=True, key=lambda x: x[0])
        return maxPaths
    
    
    # Método para obtener todas las componentes conexas
    def get_components(self):
        visit = [False] * self.n
        components = []
        for u in range(self.n):
            if not visit[u]:
                component = []
                self.__DFS_collect(u, visit, component)
                components.append(component)
        return components

    def kruskal_mst_component(self, component):
        mst = []
        mst_weight = 0

        # Lista de todas las aristas en la componente
        edges = []
        for u in component:
            for v, weight in self.L[u]:
                if u < v and v in component:  # Evitar duplicar aristas en grafos no dirigidos
                    edges.append((weight, u, v))

        # Ordenar aristas por peso
        edges.sort()

        # Crear un DisjointSet para la componente
        disjoint_set = DisjointSet(self.n)

        # Aplicar Kruskal para la componente
        for weight, u, v in edges:
            if disjoint_set.find(u) != disjoint_set.find(v):
                mst.append((u, v, weight))
                mst_weight += weight
                disjoint_set.union(u, v)

        return mst_weight, mst

    def kruskal_mst_all_components(self):
        components = self.get_components()
        total_mst_weight = 0
        mst_per_component = []

        # Calcular el MST para cada componente
        for i, component in enumerate(components):
            mst_weight, mst = self.kruskal_mst_component(component)
            total_mst_weight += mst_weight
            mst_per_component.append((mst_weight, mst))
            print(f"Peso del MST de la componente {i + 1}: {round(mst_weight,2)}")
            #print("Aristas en el MST de la componente:")
            #for u, v, weight in mst:
            #    print(f"{u} -- {v} (peso: {weight})")

        print(f"Peso total de los MST de todas las componentes: {total_mst_weight}")
        return mst_per_component
    