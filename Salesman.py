# Salesman.py
# Main Function - manages control flow
import GeneticAlgoritmManager import Manager
from Graph import Graph

def importGraph(fileName):
    # Imports the graph information from a textfile and stores it in a Graph object
    filein = open(fileName)
    data = filein.read()

    linesin = [ sublist.strip().split() for sublist in data.splitlines() ]
    vertexCount = int(linesin[0][0])
    linesin.pop(0)
    edges = [(int(edge[0]), int(edge[1]), int(edge[2])) for edge in linesin]

    newGraph = Graph(vertexCount, edges)

    return newGraph

# import graph data and create the Genetic Algorithm manager
citiesGraph = importGraph('salesman.txt')
manager = Manager(citiesGraph)

for case in range(manager.crossoverCount):
    manager.runAlgorithm(case)