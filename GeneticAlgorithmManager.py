# GeneticAlgorithmManager.py
# Maintains all functions for performing the genetic algorithm
from Classes import Solution, Metrics
import Display
import time
import os
import random
import operator
import collections
import copy


class Manager:
    firstGenerationSize = 4096                      # the size of the first generation of solutions
    crossoverNames = {                              # For Display purposes: the names of implemented crossover functions
            0: "Ordered Crossover",
            1: "Partially Mapped Crossover",
            2: "Maximal Preservative Crossover",
            3: "Alternating Crossover",
            4: "Edge Recombination Crossover",
            5: "Sorted Match Crossover"
    }
    crossoverCount = len(crossoverNames)            # the number of crossover functions the manager has implemented

    # Initialization Functions
    # Create and return the first generation of solutions
    def generate_solutions(self, first_generation_size):
        generated = []
        for _ in range(first_generation_size):
            path = list(self.graph.vertices)         # Create a copy of the vertex list
            random.shuffle(path)                # Shuffle the vertex list: creating a random path through the graph
            generated.append(Solution(path))    # Append to the initial solution set
        return generated

    # Resets the first generation of solutions. Used for extended simulations.
    def reset_first_generation(self):
        self.firstGeneration = self.generate_solutions(self.firstGenerationSize)

    # Initializer
    def __init__(self, graph):
        self.graph = graph
        self.firstGeneration = self.generate_solutions(self.firstGenerationSize)    # The initial generation
        self.currentGeneration = []
        self.bestSolution = self.firstGeneration[0]     # Tracks the best generation for each function
        self.results = []   # Stores the results of each crossover. T(crossover_case, solution, generation_count)

    # EVALUATION FUNCTIONS
    # Return the cost of following the given path
    def get_cost(self, path):
        path = list(path)
        cost = 0
        for i in range(len(path)):
            j = i+1
            if j >= len(path):
                j = 0
            v1, v2 = path[i], path[j]           # get the vertices of the given indices
            cost += self.graph.weights[v1][v2]  # Retrieve the weight of the edge - add to cost
        return cost

    # Gets the cost for each solution in the generation, then sorts the solutions by cost, ascending
    def evaluate_current_generation(self):
        for solution in self.currentGeneration:
            if solution.cost == -1:     # No need to reevaluate a solution
                solution.cost = self.get_cost(solution.path)
        self.currentGeneration.sort(key=operator.attrgetter('cost'))

    # MUTATION FUNCTIONS
    # Based on a small probability, mutate the solution by swapping the values two random indices
    # Swapping values guarantees the validity of the random solution
    def attempt_mutation(self, solution):
        chance = 0.001
        if random.random() < chance:
            i, j = random.randrange(len(solution.path)), random.randrange(len(solution.path))
            temp = solution.path[i]
            solution.path[i] = solution.path[j]
            solution.path[j] = temp
        return solution

    # Calls attempt_mutation on each solution in the generation
    def mutate_generation(self):
        for i in range(len(self.currentGeneration)):
            self.currentGeneration[i] = self.attempt_mutation(self.currentGeneration[i])

    # CROSSOVER FUNCTIONS
    # Takes the length of an array and return two random indices, sorted
    # Used in many of the crossover functions
    def get_random_indices(self, length):
        start, end = 0, 0       # Values to return
        while start == end:     # Ensure that start and end are different values
            # Get start/end indices for the subsection to maintain
            start, end = random.randrange(length), random.randrange(length)

        if start > end:     # Ensure that start <= end
            temp = start
            start = end
            end = temp
        return start, end

    # Take subsections of each parent - place in children at same indices
    # Iterate over the other parent - insert values not in the subsection
    def ordered_crossover(self, solutions):
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1
            parent_x, parent_y = solutions[x].path, solutions[y].path   # Get the next set of parents

            # Execute twice to create 4 children
            for _ in range(2):
                # Get two random indices from within the array
                start, end = self.get_random_indices(len(parent_x))

                # Grab the values to be maintained from the arrays
                maintained_x, maintained_y = parent_x[start:end], parent_y[start:end]
                solution_a, solution_b = [], []

                i, j = 0, 0
                while j < len(parent_x) and i < len(parent_x):
                    if j == start:
                        # Place the subsection at the same index
                        solution_a.extend(maintained_x)
                        j += len(maintained_x)

                    # If the next value is not in the array, place it in the next empty index
                    if parent_y[i] not in maintained_x:
                        solution_a.append(parent_y[i])
                        j += 1
                    # Always increment to the next value in the parent
                    i += 1

                i, j = 0, 0
                while j < len(parent_y) and i < len(parent_y):
                    if j == start:
                        # Place the subsection at the same index
                        solution_b.extend(maintained_y)
                        j += len(maintained_y)

                    # If the next value is not in the array, place it in the next empty index
                    if parent_x[i] not in maintained_y:
                        solution_b.append(parent_x[i])
                        j += 1
                    # Always increment to the next value in the parent
                    i += 1

                # Append the children to the next generation
                generation.extend([Solution(solution_a), Solution(solution_b)])
        return generation

    # Take subsections of each parent - place in children and map to each other
    # Iterate over other parent - if vertex in subsection, place the mapped value instead
    def partially_mapped_crossover(self, solutions):
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1
            parent_x, parent_y = solutions[x].path, solutions[y].path   # Get the next set of parents

            # Execute twice to create 4 children
            for _ in range(2):
                # Get two random indices from within the array
                start, end = self.get_random_indices(len(parent_x))

                # Grab the values to be maintained from the arrays
                maintained_x, maintained_y = parent_x[start:end], parent_y[start:end]

                # Create two dictionaries to map the values in maintained to each other
                cross_section_x = collections.defaultdict(int)
                cross_section_y = collections.defaultdict(int)
                for i in range(len(maintained_x)):
                    cross_section_x[maintained_x[i]] = maintained_y[i]
                    cross_section_y[maintained_y[i]] = maintained_x[i]

                solution_a, solution_b = [], []

                # While the value in the parent is in the crosssection, get the mapped value
                # Then, append the resulting value to the child solution
                for i in range(0, start):
                    next_value_a = parent_y[i]
                    while next_value_a in cross_section_x:
                        next_value_a = cross_section_x[next_value_a]
                    solution_a.append(next_value_a)

                    next_value_b = parent_x[i]
                    while next_value_b in cross_section_y:
                        next_value_b = cross_section_y[next_value_b]
                    solution_b.append(next_value_b)

                # Append the maintained subarrays to the opposite child solution
                solution_a.extend(maintained_x)
                solution_b.extend(maintained_y)

                # Repeat the previous step for the end of the array
                for i in range(end, len(parent_x)):
                    next_value_a = parent_y[i]
                    while next_value_a in cross_section_x:
                        next_value_a = cross_section_x[next_value_a]
                    solution_a.append(next_value_a)

                    next_value_b = parent_x[i]
                    while next_value_b in cross_section_y:
                        next_value_b = cross_section_y[next_value_b]
                    solution_b.append(next_value_b)

                # Append the children to the next generation
                generation.extend([Solution(solution_a), Solution(solution_b)])
        return generation

    # Append a subsection of one parent to the child
    # Iterate through the second parent, append vertices that are not in the child
    def maximal_preservative_crossover(self, solutions):
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1

            # Execute twice to create 4 children
            for _ in range(2):
                # Get the next set of parents. Copy the path, as we need to make alterations
                parent_x, parent_y = list(solutions[x].path), list(solutions[y].path)

                # Get two random indices from within the array
                start, end = self.get_random_indices(len(parent_x))

                # Grab the values to be maintained from the arrays
                maintained_x, maintained_y = parent_x[start:end], parent_y[start:end]

                # Removed maintained values from opposite parent
                for v in maintained_y:
                    parent_x.remove(v)
                for v in maintained_x:
                    parent_y.remove(v)

                solution_a, solution_b = [], []

                # Append the maintained arrays to the children
                solution_a.extend(maintained_x)
                solution_b.extend(maintained_y)

                # Append the remaining values from the opposite parent
                solution_a.extend(parent_y)
                solution_b.extend(parent_x)

                # Append the children to the next generation
                generation.extend([Solution(solution_a), Solution(solution_b)])
        return generation

    # Alternate between each parent, appending the next vertex (if not in child)
    # Unless n is even, this crossover only results in 2 children, so execute once per pair
    def alternating_crossover(self, solutions):
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1
            parent_x, parent_y = list(solutions[x].path), list(solutions[y].path)   # Get the next set of parents

            solution_a, solution_b = [], []

            for i in range(len(parent_x)):
                # Alternate between vertices, adding missing ones to the children
                # Start with parent_x
                if parent_x[i] not in solution_a:
                    solution_a.append(parent_x[i])
                if parent_y[i] not in solution_a:
                    solution_a.append(parent_y[i])

                # Start with parent_y
                if parent_y[i] not in solution_b:
                    solution_b.append(parent_y[i])
                if parent_x[i] not in solution_b:
                    solution_b.append(parent_x[i])
            generation.extend([Solution(solution_a), Solution(solution_b)])
        return generation

    # Create a dictionary that holds every edge in both paths, combine edges to form a child solution
    # Idealy, this creates a solution that uses the edges, not vertices, as traits
    def edge_recombination_crossover(self, solutions):
        generation = []

        for x in range(0, len(solutions), 2):
            y = x+1
            parent_x, parent_y = solutions[x].path, solutions[y].path

            # Create a dictionary that maps each vertex to the vertices it shares edges with in both parents
            edges = collections.defaultdict(set)
            for i in range(len(parent_x)):
                j = i+1
                if j >= len(parent_x):
                    j = 0
                v1, v2, v3, v4 = parent_x[i], parent_x[j], parent_y[i], parent_y[j]
                edges[v1].add(v2)
                edges[v2].add(v1)
                edges[v3].add(v4)
                edges[v4].add(v3)

            for _ in range(4):  # Create 4 children
                # Copy the map
                edges_copy = copy.copy(edges)

                solution = list()

                # 1) Add a random vertex to the solution
                solution.append(random.choice(parent_x))
                done = False
                while not done:     # Repeat until every vertex is visited
                    # 2) Remove all instances of the last visted vertex from the dictionary
                    vertex = solution[-1]
                    for vertices in edges_copy.values():
                        vertices.discard(vertex)

                    # 3) If the set of the vertex isn't empty...
                    if len(edges_copy[vertex]) > 0:
                        # 4) Go to an adjacent city that has the fewest number of edges
                        adjacent = []

                        # Append vertices and edges in tuple
                        for v in edges_copy[vertex]:
                            adjacent.append((v, edges_copy[v]))

                        # Sort by length of edges, append the vertex with the fewest
                        adjacent.sort(key=lambda tup: len(tup[1]))
                        solution.append(adjacent[0][0])
                    else:
                        # 5) If all vertices visited, exit.
                        if len(solution) == len(parent_x):
                            done = True
                        else:
                            # Otherwise, select an unvisited vertex
                            repeat = True
                            while repeat:
                                v = random.choice(parent_x)
                                if v not in solution:
                                    solution.append(v)
                                    repeat = False
                generation.append(Solution(solution))
        return generation

    # Find sub-tours in each parent that:
    # a) are the same length
    # b) start and end at the same cities
    # c) contain the same cities
    # Swap these sub-tours in the parents to create children
    # These tours are found by comparing the sub-tours created by each pair of vertices
    # There are no guarantees with this crossover, so it is comprehensive in looking for children
    def sorted_match_crossover(self, solutions):
        generation = []
        for x in range(0, len(solutions), 2):
            y = x+1
            parent_x, parent_y = solutions[x].path, solutions[y].path     # Get the next set of parents

            # Get two vertices
            for i in range(len(parent_x)):
                for j in range(i, len(parent_x)):
                    # Get the indices of each vertex in each parent (verifies b)
                    x1, x2 = parent_x.index(i), parent_x.index(j)
                    y1, y2 = parent_y.index(i), parent_y.index(j)

                    # Sort indices as needed
                    if x1 > x2:
                        x1, x2 = x2, x1
                    if y1 > y2:
                        y1, y2 = y2, y1

                    # Verify a)
                    if abs(x1 - x2) == abs(y1 - y2):
                        # Verify c)
                        if sorted(parent_x[x1:x2]) == sorted(parent_y[y1:y2]):
                            solution_a, solution_b = list(parent_x), list(parent_y)     # Copy the lists

                            # Swap the sub-tours
                            solution_a[x1:x2], solution_b[y1:y2] = solution_b[y1:y2], solution_a[x1:x2]
                            generation.extend([Solution(solution_a), Solution(solution_b)])
        return generation

    # Selects the correct crossover function based on case
    def crossover_switch(self, case, solutions):
        if case == 0:
            return self.ordered_crossover(solutions)
        elif case == 1:
            return self.partially_mapped_crossover(solutions)
        elif case == 2:
            return self.maximal_preservative_crossover(solutions)
        elif case == 3:
            return self.alternating_crossover(solutions)
        elif case == 4:
            return self.edge_recombination_crossover(solutions)
        else:
            return self.sorted_match_crossover(solutions)

    # DISPLAY FUNCTION
    # Outputs the final results
    def final_display(self):
        # Clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')

        # Display each recorded result
        for result in self.results:
            print("Result for Crossover Function: " + self.crossoverNames[result[0]])
            Display.display_path(self.graph, result[1])
            print("Solution found after " + str(result[2]) + " generations")
            print()

    # 'MAIN' FUNCTIONS
    # Runs the genetic algorthm using a chosen crossover function
    def run_algorithm(self, case, wait, metrics_run, will_display):
        # Helper variables.
        max_staleness = 20   # If the best solution doesn't change for a certain number of generations, then exit
        staleness_count = 0  # Counts how many generations the best solution has existed
        gen = 0             # Tracks the number of generations the algorithm has run for

        # Reset the current generation to the intially generated first generation
        self.currentGeneration = list(self.firstGeneration)
        self.bestSolution = self.currentGeneration[0]       # Save the current best generation to determine when to exit
        keep_count = int(len(self.currentGeneration)/4)      # The number of solutions to keep after each evalutation

        while staleness_count < max_staleness:
            # Get the cost for each solution in the generation
            self.evaluate_current_generation()

            # Evaluate for staleness
            if self.bestSolution.cost == self.currentGeneration[0].cost:
                staleness_count += 1
            else:
                # New solution: update helpers
                staleness_count = 0
                self.bestSolution = self.currentGeneration[0]

            # Display current best in generation
            gen += 1
            if will_display:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Testing Crossover Function: " + self.crossoverNames[case])
                print("Current Generation: " + str(gen))
                Display.display_path(self.graph, self.currentGeneration[0])
                print("Staleness: " + str(staleness_count))
                # Debug: Ensure that solution is valid
                if sorted(self.bestSolution.path) != self.graph.vertices:
                    print("SOLUTION IS INVALID. CHECK " + self.crossoverNames[case].upper())

            # Execute Crossover on best solutions
            newGeneration = self.currentGeneration[:keep_count]                  # keep the top 25% of the generation
            random.shuffle(newGeneration)                                       # shuffle; ensures more genetic variety
            newGeneration.extend(self.crossover_switch(case, newGeneration))     # Crossover select
            self.currentGeneration = newGeneration

            # attempt mutation on each solution
            self.mutate_generation()

            if wait:
                # Wait before repeating
                time.sleep(0.20)

        # For non-metric runs, save the results of the crossover for final display
        # Otherwise, return the values for the metric object
        # Use (gen-max_staleness) to get when the bestSolution was generated
        if not metrics_run:
            self.results.append((case, self.bestSolution, gen-max_staleness))
        else:
            return (self.bestSolution, gen-max_staleness)

    # Runs the algorithm for each crossover multiple times to find best and average performance
    def run_metrics(self, case, runs):
        # Create metrics object
        data = Metrics(case)

        print("Testing Crossover Function: " + self.crossoverNames[case])

        # Run the algorithm the specified number of times
        for _ in range(runs):
            # Reset the first generation
            self.reset_first_generation()

            # Run the algorithm
            solution, generations = self.run_algorithm(case, False, True, False)

            # Append new data
            data.costs.append(solution.cost)
            data.generations.append(generations)

            # Set new bests
            if data.bestSolution is not None:
                if solution.cost < data.bestSolution.cost:
                    data.bestSolution = solution
            else:
                data.bestSolution = solution
            if generations < data.bestGeneration:
                data.bestGeneration = generations

        # Calculate averages
        data.calculate_averages()
        return data
