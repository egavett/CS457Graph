# GeneticAlgorithm.py
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
            1 : "Partially Mapped Crossover",
            2 : "Cycle Crossover"
    }
    crossoverCount = len(crossoverNames)            # the number of crossover functions the manager has implemented

    ## Initialization Functions ##
    def __init__(self, graph):
        self.graph = graph
        self.firstGeneration = generateSolutions(firstGenerationSize)   # Create and store the inital sample of solutions; start each iteration with the same data set
        self.currentGeneration = []

    # Create and return the first generation of solutions
    def generateSolutions(firstGenerationSize):
        generated = []
        for _ in range(firstGenerationSize):
            path = list(graph.vertices)         # Create a copy of the vertex list
            random.shuffle(path)                # Shuffle the vertex list: creating a random path through the graph
            generated.append(Solution(path))    # Append to the initial solution set
        return generated


    ## Evalutation and Mutation functions ##
    # Return the cost of following the given path
    def getCost():
        cost = 0
        for i in range(len(solution.path)):
            v1, v2 = solution.path[i], solution.path[i+1]   # get the vertices of the given indices - final i+1 will return index 0
            cost += graph.weight[v1][v2]                    # retrive the weight of the edge - add to cost
        return cost
    
    # Gets the cost for each solution in the generation, then sorts the solutions by cost, ascending
    def evaluateGeneration():
        for solution in self.currentGeneration:
            solution.cost = getCost(solution.path)
        self.currentGeneration.sort(key = operator.attrgetter('cost'))

    # Based on a small probability, mutate the solution by swapping the values two random indices
    # Swapping values guarantees the validity of the random solution
    def attemptMutation(solution):   
        chance = 0.0001
        if random.random() < change:
            i, j = random.randrange(len(solution))
        temp = solution[i]
        solution[i] = solution[j]
        solution[j] = temp
        return solution

    # Calls attemptMutation on each solution in the generation
    def mutateGeneration()
        for solution in self.currentGeneration:
            solution = attemptMutation(solution)


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

            i, j = 0
            while j < len(parentX):
                if j == start:
                    solutionA.extend(maintainedX)
                    j += len(maintainedX)
                else:
                    if parentY[i] not in maintainedX:
                        solutionA.append(parentY[j])
                        j += 1
                    if i == start:
                        i += len(maintainedX)
                    else:
                        i += 1
            
            i, j = 0
            while j < len(parentY):
                if j == start:
                    solutionB.extend(maintainedY)
                    j += len(maintainedY)
                    i += len(maintainedY)
                else:
                    if parentX[i] not in maintainedY:
                        solutionB.append(parentX[j])
                        j += 1
                    if i == start:
                        i += len(maintainedY)
                    else:
                        i += 1

            generation.extend([solutionA, solutionB])
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

            # Grab the values to be maintained from the arrays
            maintainedX, maintainedY = parentX[start:end], parentY[start:end]  

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
                nextValueA = parentY[i]
                while nextValueA in crosssectionX.keys:
                    nextValueA = crosssectionX[nextValueA]
                solutionA.append[nextValueA]

                nextValueB = parentX[i]
                while nextValueB in crosssectionY.keys:
                    nextValueB = crosssectionY[nextValueB]
                solutionB.append[nextValueB]

            # Append the maintained subarrays to the opposite child solution
            solutionA.extend(maintainedX)
            solutionB.extend(maintainedY)

            # Repeat the previous step for the end of the array
            for i in range(end, len(parentX)):
                nextValueA = parentY[i]
                while nextValueA in crosssectionX.keys:
                    nextValueA = crosssectionX[nextValueA]
                solutionA.append[nextValueA]

                nextValueB = parentX[i]
                while nextValueB in crosssectionY.keys:
                    nextValueB = crosssectionY[nextValueB]
                solutionB.append[nextValueB]
            
            # Append the children to the next generation
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
            0 : orderedCrossover(solutions),
            1 : partiallyMappedCrossover(solutions),
            2 : cycleCrossover(solutions)
        }[case]
    
    ## 'Main' Function ##
    # Runs the genetic algorthm using a chosen crossover function
    def runAlgorithm(case):
        print("Testing Crossover Function: " + crossoverNames[case])
        maxGeneration = 100 # the number of generations the algorithm will run for
        self.currentGeneration = list(self.firstGeneration)
        for i in range(maxGeneration):
            evaluateCurrentGeneration()

            # Display current best in generation
            print("Current Generation: " + i)
            Display.displayPath(self.graph, self.currentGeneration[0])

            # Execute Crossover on best solutions
            newGeneration = self.currentGeneration[:len(self.currentGeneration)/2]   # keep the top 50% of the generation
            newGeneration.extend(crossoverSwitch(case, newGeneration))
            self.currentGeneration = newGeneration

            # attempt mutation on each solution
            mutateGeneration()            

        # Display current best in generation
        print("Final Output")
        Display.displayPath(self.graph, self.currentGeneration[0])