# GraphGenerator.py
# Generates a text file that contains a graph that adheres to the given parameters

import random

def generateGraph():
    # Input parameters
    vertexCount = int(input("How many vertices in the graph? "))
    minWeight = int(input("What should be the minimum edge weight? "))
    maxWeight = int(input("What should be the maximum edge weight? "))

    # Create array for graph
    graph = [[-1 for x in range(vertexCount)] for y in range(vertexCount)]

    # Generate random weights for the graph
    for row in range(vertexCount):
        for column in range(row):
            weight = random.randint(maxWeight, minWeight)
            graph[row][column] = weight
            graph[column][row] = weight

    # Write to file
    fileout = open("generatedGraph.txt", "w")
    fileout.write(str(vertexCount))
    fileout.write('\n')
    for row in graph:
        fileout.write(' '.join(str(x) for x in row))
        fileout.write('\n')
    fileout.close()
    print("Graph successfully generated.")