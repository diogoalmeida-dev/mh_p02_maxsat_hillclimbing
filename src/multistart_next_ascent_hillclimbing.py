import random
import time

max_evaluations = 10000000

from utils import read_cnf, random_combination, evaluate_fitness, generate_neighbours

## implements multistart next ascent hillclimbing using 1 bit hamming distance neighbourhood
def multistart_next_ascent_hillclimbing():
    clauses, num_clauses, num_vars = read_cnf()

    best_solution = None   # store the best found
    best_fitness = -1      # initialize to something smaller than possible
    evaluations = 0
    start_time = time.process_time()

    while evaluations < max_evaluations:
        current_solution = random_combination(num_vars)
        fitness = evaluate_fitness(clauses, current_solution)
        evaluations += 1

        while True:
            if evaluations >= max_evaluations:
                break

            if fitness == num_clauses:  # global optimum found
                best_solution = (current_solution, fitness, evaluations)
                cpu_time = time.process_time() - start_time
                return best_solution, evaluations, cpu_time

            indexes = list(range(num_vars))
            random.shuffle(indexes)  # shuffle indices once
            better_found = False

            for i in indexes:
                if evaluations >= max_evaluations:
                    break

                # flip bit in-place
                current_solution[i] = 1 - current_solution[i]
                nb_fitness = evaluate_fitness(clauses, current_solution)
                evaluations += 1

                if nb_fitness > fitness:
                    fitness = nb_fitness
                    better_found = True
                    break
                else:
                    current_solution[i] = 1 - current_solution[i]  # undo flip

            if not better_found:
                break  # local optimum

        if fitness > best_fitness:         # update global best if current local optimum is better
            best_solution = (current_solution, fitness, evaluations)
            best_fitness = fitness

    cpu_time = time.process_time() - start_time
    return best_solution, evaluations, cpu_time