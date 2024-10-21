from typing import List
import heapq
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
                print(f"Componente {i + 1} tiene {len(component)} vértices: {len(component)}")
    
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


    def BFS(self, u: int):
        queue = []
        visit = [False] * self.n
        visit[u] = True
        queue.append(u)
        while queue:
            u = queue.pop(0)
            print(u, end=' ')
            for v, _ in self.L[u]:    # Ajustar para tomar solo el vértice v
                if not visit[v]:
                    visit[v] = True
                    queue.append(v)


    def degree(self, u: int) -> int:
        return len(self.L[u])

    def min_degree(self) -> int:
        min = self.n
        for u in range(self.n):
            if self.degree(u) < min:
                min = self.degree(u)
        return min

    def max_degree(self) -> int:
        max = 0
        for u in range(self.n):
            if self.degree(u) > max:
                max = self.degree(u)
        return max

    def degree_sequence(self) -> List[int]:
        seq = []
        for u in range(self.n):
            seq.append(self.degree(u))
        seq.sort(reverse = True)
        return seq

    # calcular k(g) numero de componentes conexos de g
    def number_of_components(self) -> int:
        visit = [False] * self.n
        count = 0
        for u in range(self.n):
            if not visit[u]:
                visit = self.__DFS_visit(u, visit, False)
                count += 1
        return count

    # g es conexo?

    def is_connected(self) -> bool:
        return self.number_of_components() == 1

    def is_eulerian(self) -> bool:
        for u in range(self.n):
            if self.degree(u) % 2 == 1:
                return False
        return True

    def is_semieulerian(self) -> bool:
        count = 0
        for u in range(self.n):
            if self.degree(u) % 2 == 1:
                count += 1
            if count > 2:
                return False

    def is_r_regular(self, r: int) -> bool:
        for u in range(self.n):
            if self.degree(u) != r:
                return False
        return True

    def is_complete(self) -> bool:
        for u in range(self.n):
            for v in range(self.n):
                if u != v and v not in [vertex for vertex, _ in self.L[u]]:
                    return False
        return True


    def is_acyclic(self) -> bool:
        for u in range(self.n):
            for v in self.L[u]:
                if self.path(u, v):
                    return False
        return True
    
    def prim_mst(self) -> float:
        # Si el grafo no es conexo, no se puede calcular el MST completo
        #if not self.is_connected():
        #    return "El grafo no es conexo. No se puede calcular el MST completo."
        
        # El peso total del MST
        mst_weight = 0
        visited = [False] * self.n
        min_heap = [(0, 0)]    # (peso, nodo de inicio)
        heapq.heapify(min_heap)

        # Contador para asegurarnos de que conectamos todos los nodos
        edges_used = 0

        while min_heap and edges_used < self.n:
            weight, u = heapq.heappop(min_heap)
            if visited[u]:
                    continue
            # Marcar el nodo como visitado
            visited[u] = True
            mst_weight += weight
            edges_used += 1

            # Explorar las aristas conectadas al nodo u
            for v, edge_weight in self.L[u]: # Descomponer la tupla correctamente
                if not visited[v]:
                    heapq.heappush(min_heap, (edge_weight, v))

        # Retornar el peso total del MST
        return mst_weight
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
            if distance == float('inf'):
                continue
            if len(maxPaths) < 10:
                maxPaths.append((distance,index))
            else: 
                m = 0
                for j in range(len(maxPaths)):
                    if maxPaths[j][0] < maxPaths[m][0]:
                        m = j
                if distance > maxPaths[m][0]:
                    maxPaths[m] = (distance,index)
            
        maxPaths.sort(reverse=True, key=lambda x: x[0])
        return maxPaths
    
    def longestPathsX(self,v): # no sirve, creo, o calcula los minimos no se. No lo borro para seguir probando la logica luego
        D, pad = self.dijkstra(v)
        maxPaths = [(0,v)]
        index = 0
        for i in D:
            minOfMax = []
            while len(maxPaths) > 0:
                minOfMax.append(maxPaths.pop())
                if float("inf") > i > minOfMax[-1][0]:
                    minOfMax.append((i,pad[index]))
                    break
            while len(maxPaths) < 10 and len(minOfMax) > 0:
                maxPaths.append(minOfMax.pop())
            index += 1
        
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
    

"""
 # Crear un grafo con 5 nodos
g = Graph(5)

# Agregar aristas con pesos (u, v, peso)
g.add_edge(0, 1, 2.0)
g.add_edge(0, 3, 6.0)
g.add_edge(1, 2, 3.0)
g.add_edge(1, 3, 8.0)
g.add_edge(1, 4, 5.0)
g.add_edge(2, 4, 7.0)
g.add_edge(3, 4, 9.0)
print(g.dijkstra(0))
"""
""" 
# Calcular el peso del árbol de expansión mínima
mst_weight = g.prim_mst()
print(f"El peso del Árbol de Expansión Mínima es: {mst_weight}")

g.connected_components()

print ("resultados del segundo grafo:")

# Crear un grafo con 6 nodos
g = Graph(6)

# Agregar aristas
g.add_edge(0, 1, 2.0)
g.add_edge(1, 2, 3.0)
g.add_edge(3, 4, 5.0)

# Determinar si el grafo es conexo y, si no lo es, el número de componentes
g.connected_components()
"""
"""
#PRUEBA KRUSKAL

g = Graph(7)

# Agregar aristas (ejemplo de grafo con dos componentes conexas)
g.add_edge(0, 1, 4.0)
g.add_edge(1, 2, 6.0)
g.add_edge(0, 2, 3.0)

g.add_edge(3, 4, 5.0)
g.add_edge(4, 5, 7.0)
g.add_edge(3, 5, 8.0)

# Calcular el MST de cada componente
g.kruskal_mst_all_components()
"""