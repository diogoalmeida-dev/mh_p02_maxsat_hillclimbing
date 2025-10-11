#utils.py

import random

# functions that reads the cnf file and stores variables and lists of its content
def read_cnf():
    clauses = []
    num_clauses = 0
    num_vars = 0

    with open("../cnf_files/uf250-01.cnf", "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("c"):
                continue

            if line.startswith("p"): # process header line (starts with p)
                parts = line.split()
                num_vars = int(parts[2])
                num_clauses = int(parts[3])
                continue

            clause = []             # clause lines, finish with 0
            for x in line.split():
                if x == '0': ## if 0, go next line
                    continue
                try:
                    clause.append(int(x)) ## if not append the integer
                except ValueError: ## if any char besides integers, skip line (bcs of % 0 in end of file .cnf)
                    continue

            if clause:
                clauses.append(clause)

            if len(clauses) >= num_clauses: ## stop after all clauses are read
                break

    return clauses, num_clauses, num_vars

## function to find all combinations of true/false assignments for variables
def random_combination(num_vars):
    return [random.choice([0, 1]) for _ in range(num_vars)]

# Function to find the fitness being the fitness the number of clauses satisfied by the combination
def evaluate_fitness(clauses, combination):
    fitness = 0

    for clause in clauses:

        clause_fitness = 0
        for value in clause:
            var_index = abs(value) - 1 ## normalise for clause list
            bool_value = combination[var_index]
            if value < 0: ## if literal value is below 0, the variable is negated
                bool_value = not bool_value
            if bool_value: ## if bool is true
                clause_fitness = 1
                break
        fitness += clause_fitness
    return fitness

## generates the neighbour of the current solution by flipping a bit on each value of the combination
def generate_neighbours(combination):
    neighbours = []
    for var_index in range (len(combination)): ## indexar cada true e false
        tmp_combination = list(combination) ## tran
        bool_value = (combination[var_index] + 1) % 2
        tmp_combination[var_index] = bool_value
        neighbours.append(tmp_combination)

    return neighbours