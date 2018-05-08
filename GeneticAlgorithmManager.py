# GeneticAlgorithmManager.py
# Maintains all functions for performing the genetic algorithm
from Graph import Graph
import Display

import time
import os
import random
import operator
import collections

# Helper class for storing solution information
class Solution:
    # Initializer
    def __init__(self, path):
        self.path = path
        self.cost = -1  # set cost to -1 until the solution is evaluated
        
    # Debug: for printing
    def __repr__(self):
        return "The path: {" + " ".join(str(e) for e in self.path) + "} costs: " + str(self.cost)
    def __str__(self):
        return "The path: {" + " ".join(str(e) for e in self.path) + "} costs: " + str(self.cost)
        

class Manager:
    firstGenerationSize = 64                        # the size of the first generation of solutions
    crossoverNames = {                              # For Display purposes: the names of implemented crossover functions
            1 : "Ordered Crossover",
            0 : "Partially Mapped Crossover"
            #2 : "Cycle Crossover"
    }
    crossoverCount = len(crossoverNames)            # the number of crossover functions the manager has implemented

    ## Initialization Functions ##
    # Create and return the first generation of solutions
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
        self.bestSolution = self.firstGeneration[0]     # Save the current best generation to determine when to exit

    ## Evalutation and Mutation functions ##
    # Return the cost of following the given path
    def getCost(self, path):
        path = list(path)
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
            if solution.cost == -1:     # No need to reevaluate a solution
                solution.cost = self.getCost(solution.path)
        self.currentGeneration.sort(key = operator.attrgetter('cost'))

    # Based on a small probability, mutate the solution by swapping the values two random indices
    # Swapping values guarantees the validity of the random solution
    def attemptMutation(self, solution):   
        chance = 0.0001
        if random.random() < chance:

            i, j = random.randrange(len(solution.path)), random.randrange(len(solution.path))
            temp = solution.path[i]
            solution.path[i] = solution.path[j]
            solution.path[j] = temp
        return solution

    # Calls attemptMutation on each solution in the generation
    def mutateGeneration(self):
        for solution in self.currentGeneration:
            solution = self.attemptMutation(solution)


    ## Crossover Functions ##  
    def orderedCrossover(self, solutions):
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1
            parentX, parentY = solutions[x], solutions[y]   # Get the next set of parents
            
            # Execute twice to create 4 children
            for _ in range(2):
                start, end = 0, 0
                while start == end:
                    start, end =  random.randrange(len(parentX.path)), random.randrange(len(parentX.path)) # Get start/end indices for the subarray to maintain

                if start > end: # Ensure that start <= end
                    temp = start
                    start = end
                    end = temp

                maintainedX, maintainedY = parentX.path[start:end], parentY.path[start:end]   # Grab the values to be maintained from the arrays
                solutionA, solutionB = [], []

                i, j = 0, 0
                while j < len(parentX.path) and i < len(parentX.path):
                    if j == start:
                        solutionA.extend(maintainedX)
                        j += len(maintainedX)

                    if parentY.path[i] not in maintainedX:
                        solutionA.append(parentY.path[i])
                        j += 1
                    i += 1
                
                i, j = 0, 0
                while j < len(parentY.path) and i < len(parentY.path):
                    if j == start:
                        solutionB.extend(maintainedY)
                        j += len(maintainedY)
                    
                    if parentX.path[i] not in maintainedY:
                        solutionB.append(parentX.path[i]) 
                        j += 1
                    i += 1

                # Append the children to the next generation
                generation.extend([Solution(solutionA), Solution(solutionB)])
        return generation

    def partiallyMappedCrossover(self, solutions):
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1
            parentX, parentY = solutions[x], solutions[y]   # Get the next set of parents

            # Execute twice to create 4 children
            for _ in range(2):
                start, end = 0, 0
                while start == end:
                    start, end =  random.randrange(len(parentX.path)), random.randrange(len(parentX.path)) # Get start/end indices for the subarray to maintain

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
                    while nextValueA in crosssectionX:
                        nextValueA = crosssectionX[nextValueA]
                    solutionA.append(nextValueA)

                    nextValueB = parentX.path[i]
                    while nextValueB in crosssectionY:
                        nextValueB = crosssectionY[nextValueB]
                    solutionB.append(nextValueB)

                # Append the maintained subarrays to the opposite child solution
                solutionA.extend(maintainedX)
                solutionB.extend(maintainedY)

                # Repeat the previous step for the end of the array
                for i in range(end, len(parentX.path)):
                    nextValueA = parentY.path[i]
                    while nextValueA in crosssectionX:
                        nextValueA = crosssectionX[nextValueA]
                    solutionA.append(nextValueA)

                    nextValueB = parentX.path[i]
                    while nextValueB in crosssectionY:
                        nextValueB = crosssectionY[nextValueB]
                    solutionB.append(nextValueB)
                
                # Append the children to the next generation
                generation.extend([Solution(solutionA), Solution(solutionB)])
        return generation

    def cycleCrossover(self, solutions):
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1
            parentX, parentY = solutions[x], solutions[y]   # Get the next set of parents
            
            solutionA, solutionB = [None] * len(parentX).path, [None] * len(parentX.path) # Populate with none so we can add the solutions at arbritary indices

            

            # Append the children to the next generation
            generation.extend([Solution(solutionA), Solution(solutionB)])
        return generation

    def crossoverSwitch(self, case, solutions):
        # Selects the correct crossover function based on case
        if case == 0:
            return self.orderedCrossover(solutions)
        elif case == 1:
            return self.partiallyMappedCrossover(solutions)
        else:
            return self.cycleCrossover(solutions)
    
    ## 'Main' Function ##
    # Runs the genetic algorthm using a chosen crossover function
    def runAlgorithm(self, case):
        # Helper variables. If the best solution doesn't change for a certain number of generations, then exit
        maxStaleness = 10   
        stalenessCount = 0
        i = 0

        # Reset the current generation to the intially generated first generation
        self.currentGeneration = list(self.firstGeneration)
        keepCount = int(len(self.currentGeneration)/4)
        self.bestSolution = self.currentGeneration[0]     # Save the current best generation to determine when to exit

        while stalenessCount < maxStaleness:            
            # Clear the terminal
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Testing Crossover Function: " + self.crossoverNames[case])

            # Get the cost for each solution in the generation
            self.evaluateCurrentGeneration()

            # Evaluate for staleness
            if self.bestSolution.path == self.currentGeneration[0].path:
                stalenessCount += 1
            else:
                # New solution: update helpers
                stalenessCount = 0
                self.bestSolution = self.currentGeneration[0]

            # Display current best in generation
            i += 1
            print("Current Generation: " + str(i))
            Display.displayPath(self.graph, self.currentGeneration[0])

            # Execute Crossover on best solutions
            newGeneration = self.currentGeneration[:keepCount]   # keep the top 25% of the generation
            newGeneration.extend(self.crossoverSwitch(case, newGeneration))
            self.currentGeneration = newGeneration

            # attempt mutation on each solution
            self.mutateGeneration()

            print("Staleness: " + str(stalenessCount))

            # Wait 1/4 second before repeating
            time.sleep(0.25)      