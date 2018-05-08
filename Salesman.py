# Salesman.py
# Main Function - manages control flow
from GeneticAlgorithmManager import Manager
from Graph import Graph

# Imports the graph information from a textfile and stores it in a Graph object
# File format:
    # Line 1: n, the number of vertices in the graph
    # Line {2, ... n+1): A n*n matrix of weights. Use -1 for unconnected vertices
def importGraph(fileName):
    # Open the file, extract graph data
    filein = open(fileName)
    data = filein.read()
    weights = [ sublist.strip().split() for sublist in data.splitlines() ]

    # Get the number of vertices in the graph
    vertexCount = int(weights[0][0])
    weights.pop(0)

    # Create and return a graph object
    newGraph = Graph(vertexCount, weights)
    return newGraph


# Import graph data and create the Genetic Algorithm manager
citiesGraph = importGraph('salesman1.txt')
manager = Manager(citiesGraph)

# Run the genetic algorithm for each supported crossover function
for case in range(manager.crossoverCount):
    manager.runAlgorithm(case)
    input("Press Enter to continue...")