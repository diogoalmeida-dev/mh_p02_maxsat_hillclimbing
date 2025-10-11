from multistart_next_ascent_hillclimbing import *
from variable_neighbourhood_ascent import *

# iterations of the algorithm
num_runs = 30

# implements next ascent hillclimbing using 1 bit hamming distance neighbourhood
# next ascent visits neighbourhood randomly and moves to the first neighbour that improves fitness
def next_ascent_hillclimbing():
    clauses, num_clauses, num_vars = read_cnf() ## collect file content

    initial_solution = random_combination(num_vars) ## start with a random solution
    fitness = evaluate_fitness(clauses, initial_solution) ## discover initial solution fitness

    tmp_solution = initial_solution

    evaluations = 1 ## contagem da primeira avaliacao

    start_time = time.process_time() # start cpu clock

    while True:
        if fitness == num_clauses: ## if the solution is a global optimum, break and return the solution
            break

        neighbours = generate_neighbours(tmp_solution) # generate the neighbourhood by flipping one bit in each solution
        random.shuffle(neighbours) # since its next ascent, randomize search space
        better_found = False # trigger to find local optimum

        for neighbour in neighbours: # for each neighbour
            nb_fitness = evaluate_fitness(clauses, neighbour) # discover its fitness (how many clauses are satisfied)
            evaluations += 1 # for each neighbour accessed, evaluation goes up

            if nb_fitness > fitness: ## if neighbour fitness is better than the current solution, switch to the neighbour
                fitness = nb_fitness
                tmp_solution = neighbour
                better_found = True
                break

        if not better_found:
            break

    cpu_time = time.process_time() - start_time # end cpu clock
    return tmp_solution, fitness, evaluations, cpu_time

def main():
    for x in range(num_runs):
        ## variable neighbourhood
        solution, fitness, evaluations, cpu = variable_next_ascent_hillclimbing()
        print(solution, fitness, evaluations, cpu)

        print("above is variable next ascent hillclimbing, below is mnah")

    for x in range(num_runs):
        solution, evaluations, cpu_time = multistart_next_ascent_hillclimbing()
        print(solution)

if __name__ == "__main__":
    main()