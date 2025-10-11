#variable_neighbourhood_ascent.py
# this code implements the variable neighbourhood ascent using up to 3-bit hamming distance
# it performs 30 independent runs for each problem instance uf20, uf100, uf250
# basically next ascent but when we don't find a better neighbour we up the neighbourhood by one bit
import itertools
import random
import time

from sqlalchemy import false

from src.utils import random_combination, evaluate_fitness, read_cnf, generate_neighbours

# implements next ascent hillclimbing using 1 bit hamming distance neighbourhood
# next ascent visits neighbourhood randomly and moves to the first neighbour that improves fitness
def variable_next_ascent_hillclimbing():
    clauses, num_clauses, num_vars = read_cnf() ## collect file content

    initial_solution = random_combination(num_vars) ## start with a random solution
    fitness = evaluate_fitness(clauses, initial_solution) ## discover current solution fitness

    current_solution = initial_solution

    evaluations = 1 ## contagem da primeira avaliacao

    start_time = time.process_time() # start cpu clock

    k = 1

    while k <= 3:
        if fitness == num_clauses: ## if the solution is a global optimum, break and return the solution
            break

        better_found = False
        indexes = list(range(num_vars))

        for bits_to_flip in itertools.combinations(indexes, k): # generate neighbours at Hamming distance k
            neighbour = current_solution.copy()
            for index in bits_to_flip:
                neighbour[index] = 1 - neighbour[index]

            nb_fitness = evaluate_fitness(clauses, neighbour)
            evaluations += 1

            if nb_fitness > fitness:
                fitness = nb_fitness
                better_found = True
                current_solution = neighbour
                k = 1
                break

        if not better_found:
            k += 1

    cpu_time = time.process_time() - start_time # end cpu clock
    return current_solution, fitness, evaluations, cpu_time