"""
E - dict(<V> : [<V>, <V>, ...])
Ключ - строка, идентифицирующая вершину графа
значение - список вершин, достижимых из данной
Сделать так, чтобы по графу можно было итерироваться(обходом в ширину)
"""
import collections


class GraphIterator(collections.abc.Iterator):
    def __init__(self, collection):
        self.collection = collection
        self.cursor = -1
        self.root = next(iter(collection))
        self.search_deque = collections.deque(self.root)
        self.visited = [self.root]
        self.search()

    def search(self):
        while self.search_deque:
            vertex = self.search_deque.popleft()
            for neighbour in self.collection[vertex]:
                if neighbour not in self.visited:
                    self.visited.append(neighbour)
                    self.search_deque.append(neighbour)

    def __next__(self):
        if self.cursor + 1 >= len(self.visited):
            raise StopIteration
        self.cursor += 1
        return self.visited[self.cursor]


class Graph:
    def __init__(self, E):
        self.E = E

    def __iter__(self):
        return GraphIterator(self.E)


E = {'A': ['B', 'C', 'D'], 'B': ['C'], 'C': [], 'D': ['A']}
graph = Graph(E)

for vertex in graph:
    print(vertex)
