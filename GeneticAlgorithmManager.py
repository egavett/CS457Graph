# GeneticAlgorithmManager.py
# Maintains all functions for performing the genetic algorithm
from Graph import Graph
import Display

import time
import os
import random
import operator
import collections
import math

# Helper class for storing solution information
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


# Helper class: stores long-term metrics
class Metrics:

    def __init__(self, case):
        self.case = case                # The case number for the crossover function the object tracks
        self.bestSolution = None        # The cost and path of the best solution found during this run
        self.bestGeneration = math.inf  # The shortest number generations that the crossover has run for
        self.costs = []                 # Tracks the best cost from each run
        self.generations = []           # Tracks the generation time from each run
        self.meanCost = -1
        self.medianCost =  -1
        self.meanGeneration = -1 
        self.medianCost =  -1

    # Calculates the mean and median values of costs and generations
    def calculateAverages(self):
        self.meanCost = sum(self.costs)/len(self.costs) # Calculate mean cost
        self.meanGeneration = sum(self.generations)/len(self.generations) # Calculate mean generation time

        sortedCosts = list(sorted(self.costs))
        self.medianCost = sortedCosts[int(len(sortedCosts)/2)]

        sortedGenerations = list(sorted(self.generations))
        self.medianCost = sortedCosts[int(len(sortedCosts)/2)]
    
    # Displays the metrics data
    def print(self):
        print("Metrics for " + Manager.crossoverNames[self.case])
        print("Best Path: " + str(self.bestSolution))
        print("Fastest Runtime : " +  str(self.bestGeneration) + " Generations")
        print("Mean Cost: " + str(self.meanCost))
        print("Median Cost: " + str(self.medianCost))
        print("Mean Runtime: " + str(self.meanGeneration) + " Generations")
        print("Median Runtime: " + str(self.meanGeneration) + " Generations")

class Manager:
    firstGenerationSize = 4096                      # the size of the first generation of solutions
    crossoverNames = {                              # For Display purposes: the names of implemented crossover functions
            0 : "Ordered Crossover",
            1 : "Partially Mapped Crossover",
            2 : "Maximal Preservative Crossover",
            3 : "Alternating Crossover"
            #3 : "Cycle Crossover"
    }
    crossoverCount = len(crossoverNames)            # the number of crossover functions the manager has implemented

    ## Initialization Functions ##
    # Resets the first generation of solutions. May be used for extened simulations.
    def resetFirstGeneration():
        self.firstGeneration = self.generateSolutions(self.firstGenerationSize)

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
        self.firstGeneration = self.generateSolutions(self.firstGenerationSize)     # Create and store the inital sample of solutions; start each iteration with the same data set
        self.currentGeneration = []
        self.bestSolution = self.firstGeneration[0]                                 # Save the current best generation to determine when to exit
        self.results = []                                                           # Stores the results of each crossover for final display. Format: Tuple(crossoverCase, solution, generationCount)

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
        chance = 0.001
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
    # Takes the length of an array and return two random indices, sorted
    def getRandomIndices(self, length):
        start, end = 0, 0   # Values to return
        while start == end: # Ensure that start and end are different values
            start, end =  random.randrange(length), random.randrange(length) # Get start/end indices for the subarray to maintain

        if start > end: # Ensure that start <= end
            temp = start
            start = end
            end = temp
        return start, end

    def orderedCrossover(self, solutions):
        random.shuffle(solutions)
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1
            parentX, parentY = solutions[x].path, solutions[y].path   # Get the next set of parents
            
            # Execute twice to create 4 children
            for _ in range(2):
                # Get two random indices from within the array
                start, end = self.getRandomIndices(len(parentX))

                maintainedX, maintainedY = parentX[start:end], parentY[start:end]   # Grab the values to be maintained from the arrays
                solutionA, solutionB = [], []

                i, j = 0, 0
                while j < len(parentX) and i < len(parentX):
                    if j == start:
                        solutionA.extend(maintainedX)
                        j += len(maintainedX)

                    if parentY[i] not in maintainedX:
                        solutionA.append(parentY[i])
                        j += 1
                    i += 1
                
                i, j = 0, 0
                while j < len(parentY) and i < len(parentY):
                    if j == start:
                        solutionB.extend(maintainedY)
                        j += len(maintainedY)
                    
                    if parentX[i] not in maintainedY:
                        solutionB.append(parentX[i]) 
                        j += 1
                    i += 1

                # Append the children to the next generation
                generation.extend([Solution(solutionA), Solution(solutionB)])
        return generation

    def partiallyMappedCrossover(self, solutions):
        random.shuffle(solutions)
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1
            parentX, parentY = solutions[x].path, solutions[y].path   # Get the next set of parents

            # Execute twice to create 4 children
            for _ in range(2):
                # Get two random indices from within the array
                start, end = self.getRandomIndices(len(parentX))

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
                # Then, append the resulting value to the child solution
                for i in range(0, start):
                    nextValueA = parentY[i]
                    while nextValueA in crosssectionX:
                        nextValueA = crosssectionX[nextValueA]
                    solutionA.append(nextValueA)

                    nextValueB = parentX[i]
                    while nextValueB in crosssectionY:
                        nextValueB = crosssectionY[nextValueB]
                    solutionB.append(nextValueB)

                # Append the maintained subarrays to the opposite child solution
                solutionA.extend(maintainedX)
                solutionB.extend(maintainedY)

                # Repeat the previous step for the end of the array
                for i in range(end, len(parentX)):
                    nextValueA = parentY[i]
                    while nextValueA in crosssectionX:
                        nextValueA = crosssectionX[nextValueA]
                    solutionA.append(nextValueA)

                    nextValueB = parentX[i]
                    while nextValueB in crosssectionY:
                        nextValueB = crosssectionY[nextValueB]
                    solutionB.append(nextValueB)
                
                # Append the children to the next generation
                generation.extend([Solution(solutionA), Solution(solutionB)])
        return generation

    def maximalPreservativeCrossover(self, solutions):
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1

            # Execute twice to create 4 children
            for _ in range(2):
                parentX, parentY = list(solutions[x].path), list(solutions[y].path)   # Get the next set of parents. Copy the path, as we need to make alterations

                # Get two random indices from within the array
                start, end = self.getRandomIndices(len(parentX))

                # Grab the values to be maintained from the arrays
                maintainedX, maintainedY = parentX[start:end], parentY[start:end]  

                # Removed maintained values from opposite parent
                for v in maintainedY:
                    parentX.remove(v)
                for v in maintainedX:
                    parentY.remove(v)

                solutionA, solutionB = [], []

                # Append the maintained arrays to the children
                solutionA.extend(maintainedX)
                solutionB.extend(maintainedY)

                # Append the remaining values from the opposite parent
                solutionA.extend(parentY)
                solutionB.extend(parentX)

                # Append the children to the next generation
                generation.extend([Solution(solutionA), Solution(solutionB)])
        return generation

    # Alternate
    # Unless n is even, this crossover only results in 2 children, so execute once per pair
    def alternatingCrossover(self, solutions):
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1
            parentX, parentY = solutions[x].path, solutions[y].path   # Get the next set of parents

            solutionA, solutionB = [], []
            
            for i in range(len(parentX)):
                # Alternate between vertices, adding missing ones to the children
                # Start with parentX
                if parentX[i] not in solutionA:
                    solutionA.append(parentX[i])
                if parentY[i] not in solutionA:
                    solutionA.append(parentY[i])
                
                # Start with parentY
                if parentY[i] not in solutionB:
                    solutionB.append(parentY[i])
                if parentX[i] not in solutionB:
                    solutionB.append(parentX[i])
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
        elif case == 2:
            return self.maximalPreservativeCrossover(solutions)
        elif case == 3:
            return self.alternatingCrossover(solutions)
        else:
            return self.cycleCrossover(solutions)
    
    ## Display Function ##
    # Outputs the final results
    def finalDisplay(self):
        # Clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')

        # Display each recorded result
        for result in self.results:
            print("Result for Crossover Function: " + self.crossoverNames[result[0]])
            Display.displayPath(self.graph, result[1])
            print("Solution found after " + str(result[2]) + " generations")
            print()


    ## 'Main' Functions ##
    # Runs the genetic algorthm using a chosen crossover function
    def runAlgorithm(self, case, wait, metricsRun, willDisplay):
        # Helper variables. 
        maxStaleness = 20   # If the best solution doesn't change for a certain number of generations, then exit
        stalenessCount = 0  # Counts how many generations the best solution has existed
        gen = 0             # Tracks the number of generations the algorithm has run for

        # Reset the current generation to the intially generated first generation
        self.currentGeneration = list(self.firstGeneration)
        self.bestSolution = self.currentGeneration[0]       # Save the current best generation to determine when to exit
        keepCount = int(len(self.currentGeneration)/4)      # The number of solutions to keep after each evalutation

        while stalenessCount < maxStaleness:            
            

            # Get the cost for each solution in the generation
            self.evaluateCurrentGeneration()

            # Evaluate for staleness
            if self.bestSolution.cost == self.currentGeneration[0].cost:
                stalenessCount += 1
            else:
                # New solution: update helpers
                stalenessCount = 0
                self.bestSolution = self.currentGeneration[0]

            # Display current best in generation
            gen += 1
            if willDisplay:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Testing Crossover Function: " + self.crossoverNames[case])
                print("Current Generation: " + str(gen))
                Display.displayPath(self.graph, self.currentGeneration[0])
                print("Staleness: " + str(stalenessCount))

            # Execute Crossover on best solutions
            newGeneration = self.currentGeneration[:keepCount]   # keep the top 25% of the generation
            newGeneration.extend(self.crossoverSwitch(case, newGeneration))
            self.currentGeneration = newGeneration

            # attempt mutation on each solution
            self.mutateGeneration()

            if wait:
                # Wait 1/5 second before repeating
                time.sleep(0.20) 

        # For non-metric runs, save the results of the crossover for final display
        # Otherwise, return the values for the metric object
        # Use (gen-maxStaleness) to get when the bestSolution was generated
        if not metricsRun:
            self.results.append((case, self.bestSolution, gen-maxStaleness))
        else:
            return (self.bestSolution, gen-maxStaleness)

    # Runs the algorithm for each crossover multiple times to find best and average performance
    def runMetrics(self, case, runs):
        # Create metrics object
        data = Metrics(case)

        print("Testing Crossover Function: " + self.crossoverNames[case])

        # Run the algorithm the specified number of times
        for _ in range(runs):
            solution, time = self.runAlgorithm(case, False, True, False)
            
            # Apend new data
            data.costs.append(solution.cost)
            data.generations.append(time)

            # Set new bests
            if data.bestSolution != None:
                if solution.cost < data.bestSolution.cost:
                    data.bestSolution = solution
            else:
                data.bestSolution = solution
            if time < data.bestGeneration:
                data.bestGeneration = time

        # Calculate averages
        data.calculateAverages()
        return data