# GeneticAlgorithm.py
# Maintains all functions for performing the genetic algorithm
from Graph import Graph
import random
import operator

class Solution:
    # Helper class for storing solution information
    def __init__(self, path):
        self.path = path
        self.cost = -1  # set cost to -1 until the solution is evaluated

class Manager:
    firstGenerationSize = 50    # the size of the first generation of solutions
    crossoverCount = 1          # the number of crossover functions the manager has implemented

    ## Initialization Functions
    def __init__(self, graph):
        self.graph = graph
        self.firstGeneration = generateSolutions(firstGenerationSize)
        self.currentGenration = []

    def generateSolutions(firstGenerationSize):
        # Create and return the first generation of solutions
        generated = []
        for _ in range(firstGenerationSize):
            path = list(graph.vertices)
            random.shuffle(path)
            generated.append(Solution(path))
        return generated


    ## Evalutation and Mutation functions
    def getCost():
        # return the cost of following the given path
        cost = 0
        for i in range(len(solution.path)):
            v1, v2 = solution.path[i], solution.path[i+1]   # get the vertices of the given indices - final i+1 will return index 0
            cost += graph.weights[(v1, v2)]                 # retrive the weight of the edge - add to cost
        return cost
    
    def evaluateGeneration():
        # Gets the cost for each solution in the generation, then sorts the solutions by cost, ascending
        for solution in self.currentGenration:
            solution.cost = getCost(solution.path)

            
        self.currentGenration.sort(key = operator.attrgetter('cost'))

    def attemptMutation(solution):
        # Based on a small probability, mutate the solution by swapping the values two random indices
        # Swapping values guarantees the validity of the random solution
        chance = 0.0001
        if random.random() < change:
            i, j = random.randrange(len(solution))
        temp = solution[i]
        solution[i] = solution[j]
        solution[j] = temp
        return solution

    def mutateGeneration()
        # calls attemptMutation on each solution in the generation
        for solution in self.currentGenration:
            solution = attemptMutation(solution)

    ## Crossover Functions ##    
    def foo(solutions):
        # temp function for testing 
        return 1

    def crossoverSwitch(case, solutions):
        # A switch statement workaround that 
        return {
            0 : foo(solutions)
        }[case]

    
    ## 'Main' Function ##
    def runAlgorithm(case):
        # Runs the genetic algorthm using a chosen crossover function
        maxGeneration = 100 # the number of generations the algorithm will run for
        self.currentGenration = list(self.firstGeneration)
        for _ in range(maxGeneration):
            evaluateCurrentGeneration()
            # TODO: display current best in generation

            # Execute Crossover on best solutions
            newGeneration = self.currentGenration[:len(self.currentGenration)/10]   # keep the top 10% of the generation
            newGeneration = crossoverSwitch(case, newGeneration)
            self.currentGenration = newGeneration

            # attempt mutation on each solution
            mutateGeneration()            

        # TODO: display best solution