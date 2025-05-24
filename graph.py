import math
import random
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
    
    def has_edge(self, u, v):
        return self.graph[u][v] == 1
    
    def get_neighbors(self, u):
        neighbors = []
        for v in range(self.V):
            if self.graph[u][v] == 1:
                neighbors.append(v)
        return neighbors
    
    def export_to_tikz(self, layout="circle", radius=3):
        tikz = [
            "\\begin{tikzpicture}[scale=1.2, every node/.style={circle, draw, minimum size=8mm, font=\\large}]"
        ]

        positions = {}

        if layout == "circle":
            import math
            for i in range(self.V):
                angle = 2 * math.pi * i / self.V
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                positions[i] = (x, y)
                tikz.append(f"\\node (v{i}) at ({x:.2f}, {y:.2f}) {{{i}}};")
        else:
            # Alternatywnie: siatka (dla dużych grafów)
            for i in range(self.V):
                x = (i % 5) * 1.5
                y = -(i // 5) * 1.5
                positions[i] = (x, y)
                tikz.append(f"\\node (v{i}) at ({x:.2f},{y:.2f}) {{{i}}};")

        # Krawędzie
        for u in range(self.V):
            for v in range(u + 1, self.V):
                if self.graph[u][v] == 1:
                    tikz.append(f"\\draw (v{u}) -- (v{v});")

        tikz.append("\\end{tikzpicture}")
        return "\n".join(tikz)
        
    # def DFS_euler(self, v):
    #     visited = [False] * self.V
    #     stack = [v]
    #     euler_path = []

    #     while stack:
    #         u = stack[-1]
    #         if not visited[u]:
    #             visited[u] = True
    #             euler_path.append(u)
    #         found = False
    #         for neighbor in range(self.V):
    #             if self.graph[u][neighbor] == 1 and not visited[neighbor]:
    #                 stack.append(neighbor)
    #                 found = True
    #                 break
    #         if not found:
    #             stack.pop()
        
    #     return euler_path
    
    def roberts_flores_hamiltonian_cycle(self):
        n = self.V
        visited = [False] * n
        path = [-1] * n

        def hamiltonian(v, pos):
            visited[v] = True
            path[pos] = v

            if pos == n - 1:
                # Check if there is an edge from the last to the first vertex
                if self.graph[v][path[0]] == 1:
                    return True
                else:
                    visited[v] = False
                    path[pos] = -1
                    return False

            for neighbor in range(n):
                if self.graph[v][neighbor] == 1 and not visited[neighbor]:
                    if hamiltonian(neighbor, pos + 1):
                        return True

            visited[v] = False
            path[pos] = -1
            return False

        # Try to find a Hamiltonian cycle starting from each vertex
        for start in range(n):
            visited = [False] * n
            path = [-1] * n
            if hamiltonian(start, 0):
                # Complete the cycle by returning to the start
                path.append(path[0])
                return path
        return None
    
    def fleury_eulerian_cycle(self, start=0):
        # Helper to count reachable vertices using DFS
        def dfs_count(u, visited):
            visited[u] = True
            count = 1
            for v in range(self.V):
                if self.graph[u][v] and not visited[v]:
                    count += dfs_count(v, visited)
            return count

        # Helper to check if edge u-v is a valid next edge
        def is_valid_next_edge(u, v):
            if self.graph[u][v] == 0:
                return False
            # If only one adjacent edge, must use it
            count = sum(self.graph[u])
            if count == 1:
                return True
            # Otherwise, check if removing edge would disconnect the graph
            visited = [False] * self.V
            count1 = dfs_count(u, visited)
            self.remove_edge(u, v)
            visited = [False] * self.V
            count2 = dfs_count(u, visited)
            self.add_edge(u, v)
            return count1 == count2

        # Check all vertices have even degree
        for u in range(self.V):
            if sum(self.graph[u]) % 2 != 0:
                return None

        # Copy the graph so we can remove edges
        temp_graph = [row[:] for row in self.graph]
        path = []

        def fleury(u):
            for v in range(self.V):
                if temp_graph[u][v] and is_valid_next_edge(u, v):
                    temp_graph[u][v] = 0
                    temp_graph[v][u] = 0
                    fleury(v)
            path.append(u)

        # Patch remove_edge/add_edge for temp_graph
        def remove_edge(u, v):
            temp_graph[u][v] = 0
            temp_graph[v][u] = 0

        def add_edge(u, v):
            temp_graph[u][v] = 1
            temp_graph[v][u] = 1

        # Patch is_valid_next_edge to use temp_graph
        def is_valid_next_edge(u, v):
            if temp_graph[u][v] == 0:
                return False
            count = sum(temp_graph[u])
            if count == 1:
                return True
            visited = [False] * self.V
            def dfs_count_temp(u, visited):
                visited[u] = True
                count = 1
                for w in range(self.V):
                    if temp_graph[u][w] and not visited[w]:
                        count += dfs_count_temp(w, visited)
                return count
            count1 = dfs_count_temp(u, visited)
            remove_edge(u, v)
            visited = [False] * self.V
            count2 = dfs_count_temp(u, visited)
            add_edge(u, v)
            return count1 == count2

        fleury(start)
        path.reverse()
        return path
    
    # def generate_random_hamiltonian_graph(self, n, saturation_percent):
    #     import random
    #     for i in range(n):
    #         self.add_edge(i, (i + 1) % n)  # Create a cycle
    #     edges_needed = int((saturation_percent / 100) * (n * (n - 1) / 2))
    #     existing_edges = n
    #     while existing_edges < edges_needed:
    #         u = random.randint(0, n-1)
    #         v = random.randint(0, n-1)
            

    def generate_hamilton_graph(self, n, saturation_percent):
        import random
        self.V = n
        self.graph = [[0 for _ in range(n)] for _ in range(n)]

        saturation = saturation_percent / 100
        max_edges = n * (n - 1) // 2
        target_edges = int(saturation * max_edges)

        # 1. Cykl Hamiltona
        nodes = list(range(n))
        random.shuffle(nodes)
        for i in range(n):
            self.add_edge(nodes[i], nodes[(i + 1) % n])
        edges_added = n

        # 2. Krawędzie dodatkowe — krótkie cykle, parzysty stopień
        def degree(v):
            return sum(self.graph[v])

        all_possible_edges = [(i, j) for i in range(n) for j in range(i + 1, n)
                            if self.graph[i][j] == 0]
        random.shuffle(all_possible_edges)

        while edges_added < target_edges and all_possible_edges:
            # Spróbuj dodać trójkąt
            i, j = all_possible_edges.pop()
            if self.graph[i][j] == 0:
                # Znajdź trzeci wierzchołek, aby utworzyć trójkąt
                for k in range(n):
                    if k != i and k != j:
                        if self.graph[i][k] == 0 and self.graph[j][k] == 0:
                            self.add_edge(i, j)
                            self.add_edge(i, k)
                            self.add_edge(j, k)
                            edges_added += 3
                            break

    def generate_non_hamilton_graph(self, n, saturation_percent):
        import random
        assert n >= 3, "Graf niehamiltonowski musi mieć co najmniej 3 wierzchołki"

        # 1. Utwórz graf Hamiltonowski o n wierzchołkach i 50% nasyceniu
        self.generate_hamilton_graph(n, saturation_percent)

        # 2. Znajdź wierzchołek do 'obniżenia' do stopnia 1 bez rozspójnienia grafu
        candidates = list(range(n))
        random.shuffle(candidates)

        for target in candidates:
            neighbors = [v for v in range(n) if self.graph[target][v] == 1]
            if len(neighbors) <= 1:
                continue  # już ma stopień 1 lub 0

            # Próbujemy usunąć wszystkie krawędzie oprócz jednej
            random.shuffle(neighbors)
            to_keep = neighbors[0]
            removed = neighbors[1:]

            for v in removed:
                self.remove_edge(target, v)

            if self.is_connected():
                return  # sukces: spójny graf, target ma stopień 1
            else:
                # Przywróć krawędzie i próbuj innego wierzchołka
                for v in removed:
                    self.add_edge(target, v)

        raise Exception("Nie udało się wygenerować spójnego grafu z wierzchołkiem o stopniu 1.")

    
    def is_connected(self, exclude=None):
            visited = [False] * self.V

            def dfs(u):
                visited[u] = True
                for v in range(self.V):
                    if self.graph[u][v] and not visited[v] and v != exclude:
                        dfs(v)

            start = next((i for i in range(self.V) if i != exclude and sum(self.graph[i]) > 0), None)
            if start is None:
                return False

            dfs(start)

            for i in range(self.V):
                if i != exclude and sum(self.graph[i]) > 0 and not visited[i]:
                    return False
            return True




# G = Graph_Matrix(5)
# G.generate_random_hamiltonian_graph(5, 50)
# G.display()
# print("Hamiltonian Cycle:", G.roberts_flores_hamiltonian_cycle())
# print("Eulerian Cycle:", G.fleury_eulerian_cycle(0))
# G = Graph_Matrix(5)
# G.generate_random_non_hamiltonian_graph(5, 50)
# G.display()
# print("Hamiltonian Cycle:", G.roberts_flores_hamiltonian_cycle())
# print("Eulerian Cycle:", G.fleury_eulerian_cycle(0))

