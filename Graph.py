# graph.py
# Weighted, Undirected Graph Class Implementation
class Graph:
    def __init__(self, verticies, weights):
        self.verticies = [ v for v in range (verticies) ]                 # An array of vertices
        self.weights = [[-1 for x in range(verticies)] for y in range(verticies)]  # Weighted Adjacency matrix; default weight of -1 for unconnected vertices

        for row in range(len(weights)):
            for column in range(row):
                self.weights[row][column] = int(weights[row][column])