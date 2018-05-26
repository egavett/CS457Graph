# Salesman.py
# Main Function - manages control flow
from GeneticAlgorithmManager import Manager
from Graph import Graph
import GraphGenerator


# Imports the graph information from a textfile and stores it in a Graph object
# File format:
# Line 1: n, the number of vertices in the graph
# Line {2, ... n+1): A n*n matrix of weights. Use -1 for unconnected vertices
def import_graph(file_name):
    # Open the file, extract graph data
    filein = open(file_name)
    lines_in = filein.read()
    weights = [sublist.strip().split() for sublist in lines_in.splitlines()]

    # Get the number of vertices in the graph
    vertex_count = int(weights[0][0])
    weights.pop(0)

    # Create and return a graph object
    new_graph = Graph(vertex_count, weights)
    return new_graph


if __name__ == '__main__':
    # Get User Preferences

    # Generate new Graph?
    willGenerate = input("Generate a new graph before starting? (No => 0; Yes => 1) ")

    if int(willGenerate) == 1:
        GraphGenerator.generate_graph()

    # Metric Run?
    mr = input("Would you like to calculate the metrics, or see a demonstration? (0 => demonstration; 1 => metrics) ")
    runs = 1
    metricsRun = False
    willWait = False
    willDisplay = False
    if int(mr) == 1:
        metricsRun = True
        runs = int(input("How many times would you like the algorithm run for? "))
    else:
        # Show Display?
        d = input("Would you like to see the graph and path while the algorithm runs? (No => 0; Yes => 1) ")
        if int(d) == 1:
            willDisplay = 1

            # Slowed Display?
            wait = input("Would you like the algorithm to wait momentarily after each generation? (No => 0; Yes => 1) ")
            if int(wait) == 1:
                willWait = True

    # Import graph data and create the Genetic Algorithm manager
    citiesGraph = import_graph('generatedGraph.txt')
    manager = Manager(citiesGraph)

    allData = []
    for case in range(manager.crossoverCount):

        if metricsRun:
            # Find and print the metrics data for the crossover
            data = manager.run_metrics(case, runs)
            data.print()
            allData.append(data)
        else:
            # Run the genetic algorithm for each supported crossover function
            manager.run_algorithm(case, willWait, metricsRun, willDisplay)
            if willDisplay:
                input("Press Enter to continue...")

    # Display the final metrics
    if metricsRun:
        for data in allData:
            data.print()
    else:
        # Display the results of the algorithm
        manager.final_display()
