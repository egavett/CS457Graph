# Display.py
# displays graphical data
import Graph
import GeneticAlgorithmManager

import sys
from termcolor import colored

# TODO: Replace with GUI
def displayPath(graph, solution):
    vertexCount = len(solution.path)
    highlight = [[False for x in range(vertexCount)] for y in range(vertexCount)]    # 2D-array of booleans, signifies which edges are in the path

    for i in range(len(solution.path)):
        j = i+1
        if j >= len(solution.path):
            j = 0
        v1, v2 = solution.path[i], solution.path[j]   # get the vertices of the given indices
        highlight[v1][v2] = True                        # Mark the edge as being on the path

    # Print the graph, highlighting the edges that are in the path
    for row in range(len(graph.weights)):
        sys.stdout.write('| ')
        for column in range(len(graph.weights)):
        # If the edge is in the path, print green; otherwise print normally
            text = str(graph.weights[row][column])
            if highlight[row][column]:
                text = colored(graph.weights[row][column], 'green')
            sys.stdout.write(text)
            sys.stdout.write(" ")
        sys.stdout.write('| ')
        print("")
    print(solution)