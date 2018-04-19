# graph.py
# Weighted, Undirected Graph Class Implementation
class Graph:
    def __init__(self, vertices, edges):
        self.verticies = [ v for v in range (1, verticies +1) ]
        self.u_graph = collections.defaultdict(set)
        self.weights = collections.defaultdict(int)
        for edge in edges :
            # Add edges
            u_graph[edge[0]].add(edge[1])
            u_graph[edge[1]].add(edge[0])
            # Assign weights to edges
            weights[(edge[0], edge[1])] = edge[2]
            weights[(edge[1], edge[0])] = edge[2]