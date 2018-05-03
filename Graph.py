# graph.py
# Weighted, Undirected Graph Class Implementation
class Graph:
    def __init__(self, vertices, weights):
        self.verticies = [ v for v in range (verticies) ]                 # An array of vertices
        self.weights = [[0 for x in range(vertices)] for y in range(vertices)]  # Weighted Adjacency matrix

        for w in weights:
            for i in len(w):
                self.weights[w][i] = weights[w][i]