# GraphGenerator.py
# Generates a text file that contains a graph that adheres to the given parameters
import random


def generate_graph():
    # Input parameters
    vertex_count = int(input("How many vertices in the graph? "))
    min_weight = int(input("What should be the minimum edge weight? "))
    max_weight = int(input("What should be the maximum edge weight? "))

    # Create array for graph
    graph = [[-1 for _ in range(vertex_count)] for _ in range(vertex_count)]

    # Generate random weights for the graph
    for row in range(vertex_count):
        for column in range(row):
            weight = random.randint(min_weight, max_weight)
            graph[row][column] = weight
            graph[column][row] = weight

    # Write to file
    fileout = open("generatedGraph.txt", "w")
    fileout.write(str(vertex_count))
    fileout.write('\n')
    for row in graph:
        fileout.write(' '.join(str(x) for x in row))
        fileout.write('\n')
    fileout.close()
    print("Graph successfully generated.")
