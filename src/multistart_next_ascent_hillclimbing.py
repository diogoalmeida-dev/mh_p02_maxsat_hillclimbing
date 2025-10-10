import random
import time

max_evaluations = 10000000

from utils import read_cnf, random_combination, evaluate_fitness, generate_neighbours

## implements multistart next ascent hillclimbing using 1 bit hamming distance neighbourhood
def multistart_next_ascent_hillclimbing():
    clauses, num_clauses, num_vars = read_cnf()  ## collect file content

    solutions =[]

    evaluations = 0 ## contagem da primeira avaliacao

    start_time = time.process_time()  # start cpu clock

    while evaluations < max_evaluations:
        initial_solution = random_combination(num_vars)  ## start with a random solution
        fitness = evaluate_fitness(clauses, initial_solution)  ## discover initial solution fitness
        evaluations += 1
        tmp_solution = initial_solution

        if fitness == num_clauses:  ## if the solution is a global optimum, break and return the solution
            solutions.append(tmp_solution)
            cpu_time = time.process_time() - start_time
            return solutions, evaluations, cpu_time

        neighbours = generate_neighbours(tmp_solution)  # generate the neighbourhood by flipping one bit in each solution
        random.shuffle(neighbours)  # since its next ascent, randomize search space
        better_found = False  # trigger to find local optimum

        for neighbour in neighbours:  # for each neighbour
            nb_fitness = evaluate_fitness(clauses, neighbour)  # discover its fitness (how many clauses are satisfied)
            evaluations += 1  # for each neighbour accessed, evaluation goes up

            if nb_fitness > fitness:  ## if neighbour fitness is better than the current solution, switch to the neighbour
                fitness = nb_fitness
                tmp_solution = neighbour
                better_found = True
                break

        if not better_found:
            solution = tmp_solution
            tuple = (solution, fitness, evaluations)
            solutions.append(tuple)
            break

    cpu_time = time.process_time() - start_time  # end cpu clock
    return solutions, cpu_time