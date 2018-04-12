# GeneticAlgorithm.py
# Maintains all functions for performing the genetic algorithm
import Graph
import random

class Solution:
    # Helper class for storing solution information
    def __init__(self, path):
        self.path = path
        self.cost = -1  # set cost to -1 until the solution is evaluated

class Manager:
    def __init__(self, graph):
        self.graph = graph
        firstGenerationSize = 50  # the size of the first generation of solutions
        self.solutions = generateSolutions(firstGenerationSize)

    def generateSolutions(firstGenerationSize):
        # Create and return the first generation of solutions
        generated = []
        for _ in range(firstGenerationSize):
            path = list(graph.vertices)
            random.shuffle(path)
            generated.append(Solution(path))
        return generated

    def getCost(solution):
        # return the cost of following the given path
        cost = 0
        for i in range(len(solution.path)):
            v1, v2 = solution.path[i], solution.path[i+1]   # get the vertices of the given indices - final i+1 will return index 0
            cost += graph.weights[(v1, v2)]                 # retrive the weight of the edge - add to cost
        return cost
    
    def evaluateGeneration():
        for sol in self.solutions:
            sol.cost = getCost(sol.path)
    