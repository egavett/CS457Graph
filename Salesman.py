# Salesman.py
# Main Function - manages control flow
import Display
import GeneticAlgoritmManager
import Graph

def importGraph(fileName):
    # Imports the graph information from a textfile and stores it in a Graph object
    filein = open(fileName)
    data = filein.read()

    linesin = [ sublist.strip().split() for sublist in data.splitlines() ]
    vertexCount = int(linesin[0][0])
    linesin.pop(0)
    edges = [(int(edge[0]), int(edge[1]), int(edge[2])) for edge in linesin]

    newGraph = graph.Graph(vertexCount, edges)

    return newGraph

citiesGraph = importGraph('salesman.txt')
manager = GeneticAlgoritmManager.Manager(citiesGraph)

