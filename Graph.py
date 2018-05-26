# graph.py
# Weighted, Undirected Graph Class Implementation


class Graph:
    def __init__(self, vertices, weights):
        self.vertices = [v for v in range(vertices)]                 # An array of vertices
        # Weighted Adjacency matrix; default weight of -1 for unconnected vertices
        self.weights = [[-1 for _ in range(vertices)] for _ in range(vertices)]

        for row in range(len(weights)):
            for column in range(len(weights)):
                self.weights[row][column] = int(weights[row][column])

    # Testing Tool: confirms that it costs the same to go between two vertices in either direction
    def check_validity(self):
        for row in range(len(self.weights)):
            for column in range(row):
                if self.weights[row][column] != self.weights[column][row]:
                    print("Discrepancy between (" +
                          str(row) + ", " + str(column) +
                          ") and (" + str(column) + ", " + str(row) + ")")

        input("Press enter to continue...")
