class Graph_Matrix:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]
        
    def add_edge(self, u, v):
        self.graph[u][v] = 1
        self.graph[v][u] = 1
        
    def remove_edge(self, u, v):
        self.graph[u][v] = 0
        self.graph[v][u] = 0
        
    def display(self):
        for row in self.graph:
            print(" ".join(str(x) for x in row))
    
    def has_esdge(self, u, v):
        return self.graph[u][v] == 1
    
    def get_neighbors(self, u):
        neighbors = []
        for v in range(self.V):
            if self.graph[u][v] == 1:
                neighbors.append(v)
        return neighbors
    
    def DFS_euler(self, v):
        visited = [False] * self.V
        stack = [v]
        euler_path = []

        while stack:
            u = stack[-1]
            if not visited[u]:
                visited[u] = True
                euler_path.append(u)
            found = False
            for neighbor in range(self.V):
                if self.graph[u][neighbor] == 1 and not visited[neighbor]:
                    stack.append(neighbor)
                    found = True
                    break
            if not found:
                stack.pop()
        
        return euler_path
    
Graph = Graph_Matrix(5)
for i in range(5):
    Graph.add_edge(i, (i + 1) % 5)
Graph.display()
print(Graph.DFS_euler(0))
    
    