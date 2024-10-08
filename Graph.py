from typing import List

class Graph:
  def __init__ (self, n: int, directed: bool = False):
    self.n = n
    self.directed = directed
    self.L: List[List[int]] = [[] for _ in range(n)]

  def add_edge(self, u: int, v: int) -> bool:
    if 0 <= u < self.n and 0 <= v < self.n:
      self.L[u].append(v)
      self.L[u].sort()
      if not self.directed:
        self.L[v].append(u)
        self.L[v].sort()
      return True
    return False

  def DFS(self, u: int) -> None:
    visit = [False for _ in range(self.n)]
    self.__DFS_visit(u, visit)
    print()

  def __DFS_visit(self, u: int, visit: List[bool], Print: bool = True) -> List:
    visit[u] = True
    if Print:
      print(u, end=' ')
    for v in self.L[u]:
      if not visit[v]:
        visit = self.__DFS_visit(v, visit, Print)
    return visit

  def BFS(self, u:int):
    queue = []
    visit = [False] * self.n
    visit[u] = True
    queue.append(u)
    while queue:
      u = queue.pop(0)
      print(u, end=' ')
      for v in self.L[u]:
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
        if u != v and self.degree(u) != self.degree(v):
          return False
    return True

  def is_acyclic(self) -> bool:
    for u in range(self.n):
      for v in self.L[u]:
        if self.path(u, v):
          return False
    return True
