# GeneticAlgorithmManager.py
# Maintains all functions for performing the genetic algorithm
from Graph import Graph
import Display

import random
import operator
import collections

# Helper class for storing solution information
class Solution:
    def __init__(self, path):
        self.path = path
        self.cost = -1  # set cost to -1 until the solution is evaluated

class Manager:
    firstGenerationSize = 50                        # the size of the first generation of solutions
    crossoverNames = {                              # For Display purposes: the names of implemented crossover functions
            0 : "Ordered Crossover",
            1 : "Partially Mapped Crossover"
            #2 : "Cycle Crossover"
    }
    crossoverCount = len(crossoverNames)            # the number of crossover functions the manager has implemented

    ## Initialization Functions ##
    # Create and return the first generation of solutions
  #@staticmethod
    def generateSolutions(self, firstGenerationSize):
        generated = []
        for _ in range(firstGenerationSize):
            path = list(self.graph.verticies)         # Create a copy of the vertex list
            random.shuffle(path)                # Shuffle the vertex list: creating a random path through the graph
            generated.append(Solution(path))    # Append to the initial solution set
        return generated

    # Initializer
    def __init__(self, graph):
        self.graph = graph
        self.firstGeneration = self.generateSolutions(self.firstGenerationSize)   # Create and store the inital sample of solutions; start each iteration with the same data set
        self.currentGeneration = []

    ## Evalutation and Mutation functions ##
    # Return the cost of following the given path
    def getCost(self, path):
        cost = 0
        for i in range(len(path)):
            j = i+1
            if j >= len(path):
                j = 0
            v1, v2 = path[i], path[j]   # get the vertices of the given indices
            cost += self.graph.weights[v1][v2]                    # retrive the weight of the edge - add to cost
        return cost
    
    # Gets the cost for each solution in the generation, then sorts the solutions by cost, ascending
    def evaluateCurrentGeneration(self):
        for solution in self.currentGeneration:
            solution.cost = self.getCost(solution.path)
        self.currentGeneration.sort(key = operator.attrgetter('cost'))

    # Based on a small probability, mutate the solution by swapping the values two random indices
    # Swapping values guarantees the validity of the random solution
    def attemptMutation(self,solution):   
        chance = 0.0001
        if random.random() < change:
            i, j = random.randrange(len(solution))
        temp = solution[i]
        solution[i] = solution[j]
        solution[j] = temp
        return solution

    # Calls attemptMutation on each solution in the generation
    def mutateGeneration(self):
        for solution in self.currentGeneration:
            solution = attemptMutation(solution)


    ## Crossover Functions ##  
    def orderedCrossover(self, solutions):
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1
            parentX, parentY = solutions[x], solutions[y]   # Get the next set of parents
            start, end = random.randrange(len(parentX.path)), random.randrange(len(parentX.path)) # Get start/end indices for the subarray to maintain

            if start > end: # Ensure that start <= end
                temp = start
                start = end
                end = temp

            maintainedX, maintainedY = parentX.path[start:end], parentY.path[start:end]   # Grab the values to be maintained from the arrays
            solutionA, solutionB = [], []

            i, j = 0, 0
            while j < len(parentX.path):
                if j == start:
                    solutionA.extend(maintainedX)
                    j += len(maintainedX)
                else:
                    if parentY.path[i] not in maintainedX:
                        solutionA.append(parentY.path[j])
                        j += 1
                    if i == start:
                        i += len(maintainedX)
                    else:
                        i += 1
            
            i, j = 0
            while j < len(parentY.path):
                if j == start:
                    solutionB.extend(maintainedY)
                    j += len(maintainedY)
                    i += len(maintainedY)
                else:
                    if parentX.path[i] not in maintainedY:
                        solutionB.append(parentX.path[j])
                        j += 1
                    if i == start:
                        i += len(maintainedY)
                    else:
                        i += 1

            generation.extend([solutionA, solutionB])
        return generation

    def partiallyMappedCrossover(self, solutions):
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1
            parentX, parentY = solutions[x], solutions[y]   # Get the next set of parents
            start, end = random.randrange(len(parentX.path)), random.randrange(len(parentX.path)) # Get start/end indices for the subarray to maintain

            if start > end: # Ensure that start <= end
                temp = start
                start = end
                end = temp

            # Grab the values to be maintained from the arrays
            maintainedX, maintainedY = parentX.path[start:end], parentY.path[start:end]  

            # Create two dictionaries to map the values in maintained to each other
            crosssectionX = collections.defaultdict(int) 
            crosssectionY = collections.defaultdict(int)
            for i in range(len(maintainedX)):
                crosssectionX[maintainedX[i]] = maintainedY[i]
                crosssectionY[maintainedY[i]] = maintainedX[i]

            solutionA, solutionB = [], []

            # While the value in the parent is in the crosssection, get the mapped value
            # Then, append the initial or resulting value to the child solution
            for i in range(0, start):
                nextValueA = parentY.path[i]
                while nextValueA in crosssectionX.keys:
                    nextValueA = crosssectionX[nextValueA]
                solutionA.append[nextValueA]

                nextValueB = parentX.path[i]
                while nextValueB in crosssectionY.keys:
                    nextValueB = crosssectionY[nextValueB]
                solutionB.append[nextValueB]

            # Append the maintained subarrays to the opposite child solution
            solutionA.extend(maintainedX)
            solutionB.extend(maintainedY)

            # Repeat the previous step for the end of the array
            for i in range(end, len(parentX.path)):
                nextValueA = parentY.path[i]
                while nextValueA in crosssectionX.keys:
                    nextValueA = crosssectionX[nextValueA]
                solutionA.append[nextValueA]

                nextValueB = parentX.path[i]
                while nextValueB in crosssectionY.keys:
                    nextValueB = crosssectionY[nextValueB]
                solutionB.append[nextValueB]
            
            # Append the children to the next generation
            generation.append(solutionA)
            generation.append(solutionB)
        return generation

    def cycleCrossover(self, solutions):
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1
            parentX, parentY = solutions[x], solutions[y]   # Get the next set of parents
            
            solutionA, solutionB = [None] * len(parentX).path, [None] * len(parentX.path) # Populate with none so we can add the solutions at arbritary indices

            

            generation.append(solutionA)
            generation.append(solutionB)
        return generation

    def crossoverSwitch(self, case, solutions):
        # A switch statement workaround that executes and returns the result of the chosen crossover 
        return {
            0 : self.orderedCrossover(solutions),
            1 : self.partiallyMappedCrossover(solutions),
            2 : self.cycleCrossover(solutions)
        }[case]
    
    ## 'Main' Function ##
    # Runs the genetic algorthm using a chosen crossover function
    def runAlgorithm(self,case):
        print("Testing Crossover Function: " + self.crossoverNames[case])
        maxGeneration = 100 # the number of generations the algorithm will run for
        self.currentGeneration = list(self.firstGeneration)
        for i in range(maxGeneration):
            self.evaluateCurrentGeneration()

            # Display current best in generation
            print("Current Generation: " + str(i))
            Display.displayPath(self.graph, self.currentGeneration[0])

            # Execute Crossover on best solutions
            newGeneration = self.currentGeneration[:int(len(self.currentGeneration)/2)]   # keep the top 50% of the generation
            newGeneration.extend(self.crossoverSwitch(case, newGeneration))
            self.currentGeneration = newGeneration

            # attempt mutation on each solution
            self.mutateGeneration()            

        # Display current best in generation
        print("Final Output")
        Display.displayPath(self.graph, self.currentGeneration[0])