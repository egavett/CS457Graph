# Classes.py
# Contains helper classs for the algorithm
import math
import statistics


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


# Stores solution information
class Solution:
    # Initializer
    def __init__(self, path):
        self.path = path
        self.cost = -1  # set cost to -1 until the solution is evaluated

    # For printing
    def __repr__(self):
        return "The path: {" + " ".join(str(e) for e in self.path) + "} costs: " + str(self.cost)

    def __str__(self):
        return "The path: {" + " ".join(str(e) for e in self.path) + "} costs: " + str(self.cost)


# Stores long-term simulation metrics
class Metrics:
    # Initializer
    def __init__(self, case):
        self.case = case                # The case number for the crossover function the object tracks
        self.bestSolution = None        # The cost and path of the best solution found during this run
        self.bestGeneration = math.inf  # The shortest number generations that the crossover has run for
        self.costs = []                 # Tracks the best cost from each run
        self.generations = []           # Tracks the generation time from each run
        # Mean and median for costs and generations. Calculated at the end
        self.meanCost = -1
        self.medianCost = -1
        self.meanGeneration = -1
        self.medianGeneration = -1

    # Calculates the mean and median values of costs and generations
    def calculate_averages(self):
        self.meanCost = statistics.mean(self.costs)                 # Calculate mean cost
        self.meanGeneration = statistics.mean(self.generations)     # Calculate mean generation time
        self.medianCost = statistics.median(self.costs)             # Calculate median cost
        self.meanGeneration = statistics.median(self.generations)   # Calculate median generation time

    # Displays the metrics data
    def print(self):
        print("Metrics for " + Manager.crossoverNames[self.case])
        print("Best Path: " + str(self.bestSolution))
        print("Fastest Runtime : " + str(self.bestGeneration) + " Generations")
        print("Mean Cost: " + str(self.meanCost))
        print("Median Cost: " + str(self.medianCost))
        print("Mean Runtime: " + str(self.meanGeneration) + " Generations")
        print("Median Runtime: " + str(self.medianGeneration) + " Generations")
