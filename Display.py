# Display.py
# displays graphical data
from Graph import Graph
from GeneticAlgorithmManager import Solution
import sys
from termcolor import colored

def displayPath(graph, solution):
    vertexCount = len(solution.path)
    highlight = [False for x in range(vertexCount)] for y in range(vertexCount)]    # 2D-array of booleans, signifies which edges are in the path

    for i in range(len(solution.path)):
        v1, v2 = solution.path[i], solution.path[i+1]   # get the vertices of the given indices - final i+1 will return index 0
        highlight[v1][v2] = True                        # Mark the edge as being on the path


    # Print the graph, highlighting the edges that are in the path
    for x in graph.weights:
        print("| ")

        # If the edge is in the path, print green; otherwise print normally
        for y in line:
            if highlight[x][y]:
                text = colored(graph.weights[x][y], green)
                print 
            else:
                print(graph.weights[x][y] + " ")

        print("|")
    # Print the cost of the solutions
    print("Solution Cost: " + solution.cost)