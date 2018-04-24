# GeneticAlgorithm.py
# Maintains all functions for performing the genetic algorithm
from Graph import Graph
import random
import operator
import collections

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
        self.currentGeneration = []

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
        for solution in self.currentGeneration:
            solution.cost = getCost(solution.path)
        self.currentGeneration.sort(key = operator.attrgetter('cost'))

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
        for solution in self.currentGeneration:
            solution = attemptMutation(solution)

    def foo(solutions):
        # temp function for testing 
        return 1

    ## Crossover Functions ##    
    def orderedCrossover(solutions):
        generation = []
        for x, y in range(0, len(solutions), 2):
            parentX, parentY = solutions[x], solutions[y]   # Get the next set of parents
            start, end = random.randrange(len(parentX)), random.randrange(len(parentX)) # Get start/end indices for the subarray to maintain

            if start > end: # Ensure that start <= end
                temp = start
                start = end
                end = temp

            maintainedX, maintainedY = parentX[start:end], parentY[start:end]   # Grab the values to be maintained from the arrays
            solutionA, solutionB = [], []
            
            for i in range(0, start):
                if parentY[i] not in maintainedX:
                    solutionA.append(parentY[i])
                if parentX[i] not in maintainedY:
                    solutionB.append(parentX[i])
            
            solutionA.extend(maintainedX)
            solutionB.extend(maintainedY)

            for i in range(end, len(parentX)):
                if parentY[i] not in maintainedX:
                    solutionA.append(parentY[i])
                if parentX[i] not in maintainedY:
                    solutionB.append(parentX[i])
            generation.append(solutionA)
            generation.append(solutionB)
        return generation

    def partiallyMappedCrossover(solutions):
        generation = []
        for x, y in range(0, len(solutions), 2):
            parentX, parentY = solutions[x], solutions[y]   # Get the next set of parents
            start, end = random.randrange(len(parentX)), random.randrange(len(parentX)) # Get start/end indices for the subarray to maintain

            if start > end: # Ensure that start <= end
                temp = start
                start = end
                end = temp
            
            maintainedX, maintainedY = parentX[start:end], parentY[start:end]   # Grab the values to be maintained from the arrays

            crosssection = collections.defaultdict(int)
            for i in range(len(maintainedX)):
                crosssection[maintainedX[i]] = maintainedY[i]
                crosssection[maintainedY[i]] = maintainedX[i]

            solutionA, solutionB = [], []

            for i in range(0, start):
                if parentY[i] in crosssection.keys:
                    solutionA.append(crosssection[partyY[i]])
                else
                    solutionA.append(parentY[i])
                if parentX[i] in crosssection.keys:
                    solutionA.append(crosssection[partyX[i]])
                else
                    solutionA.append(parentX[i])

            solutionA.extend(maintainedX)
            solutionB.extend(maintainedY)

            for i in range(end, len(parentX)):
                if parentY[i] in crosssection.keys:
                    solutionA.append(crosssection[partyY[i]])
                else
                    solutionA.append(parentY[i])
                if parentX[i] in crosssection.keys:
                    solutionA.append(crosssection[partyX[i]])
                else
                    solutionA.append(parentX[i])
            
            generation.append(solutionA)
            generation.append(solutionB)
        return generation

    def cycleCrossover(solutions):
        generation = []
        for x, y in range(0, len(solutions), 2):
            parentX, parentY = solutions[x], solutions[y]   # Get the next set of parents
            
            solutionA, solutionB = [None] * len(parentX), [None] * len(parentX) # Populate with none so we can add the solutions at arbritary indices

            

            generation.append(solutionA)
            generation.append(solutionB)
        return generation

    def crossoverSwitch(case, solutions):
        # A switch statement workaround that executes and returns the result of the chosen crossover 
        return {
            0 : orderedCrossover(solutions)
            1 : partiallyMappedCrossover(solutions)
            2 : cycleCrossover(solutions)
        }[case]
    
    ## 'Main' Function ##
    def runAlgorithm(case):
        # Runs the genetic algorthm using a chosen crossover function
        maxGeneration = 100 # the number of generations the algorithm will run for
        self.currentGeneration = list(self.firstGeneration)
        for _ in range(maxGeneration):
            evaluateCurrentGeneration()
            # TODO: display current best in generation

            # Execute Crossover on best solutions
            newGeneration = self.currentGeneration[:len(self.currentGeneration)/2]   # keep the top 50% of the generation
            newGeneration.extend(crossoverSwitch(case, newGeneration))
            self.currentGeneration = newGeneration

            # attempt mutation on each solution
            mutateGeneration()            

        # TODO: display best solution