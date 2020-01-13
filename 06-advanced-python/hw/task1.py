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
        self.visited = []
        self.cc = {}
        self.search()

    def search(self):
        num_cc = 0

        for i in self.collection:
            # print(i)
            if i not in self.visited:
                num_cc += 1
                self.visited.append(i)
                self.search_deque = collections.deque(i)
                while self.search_deque:
                    vertex = self.search_deque.popleft()
                    self.cc[vertex] = num_cc
                    for neighbour in self.collection[vertex]:
                        if neighbour not in self.visited:
                            self.visited.append(neighbour)
                            self.search_deque.append(neighbour)

        print()

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


E = {'A': ['B', 'E'],
     'B': ['A', 'E'],
     'C': ['F', 'G'],
     'D': [],
     'E': ['A', 'B'],
     'F': ['C'],
     'G': ['C']}

graph = Graph(E)

for vertex in graph:
    print(vertex)
