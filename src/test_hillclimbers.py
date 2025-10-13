import time
import sys

# import algorithms
from multistart_next_ascent_hillclimbing import multistart_next_ascent_hillclimbing
from multistart_variable_neighbourhood_ascent import multistart_variable_next_ascent_hillclimbing
from variable_neighbourhood_ascent import variable_neighbourhood_hillclimbing
from next_ascent_hillclimbing import next_ascent_hillclimbing

CNF_FILES = {  # configuration
    "1": "../cnf_files/uf20-01.cnf",
    "2": "../cnf_files/uf100-01.cnf",
    "3": "../cnf_files/uf250-01.cnf"
}

def set_cnf_path(path):
    """Temporarily override the CNF file path inside utils.read_cnf()."""
    import src.utils as utils
    utils.CNF_FILE_PATH = path

def run_algorithm(choice, num_runs):
    for run in range(1, num_runs + 1):
        print(f"\n--- Run {run}/{num_runs} ---")
        if choice == "1":
            solution, fitness, evaluations, cpu_time = next_ascent_hillclimbing()
        elif choice == "2":
            solution_data, evaluations, cpu_time = multistart_next_ascent_hillclimbing()
            solution, fitness, _ = solution_data
        elif choice == "3":
            solution, fitness, evaluations, cpu_time = variable_neighbourhood_hillclimbing()
        elif choice == "4":
            solution, fitness, evaluations, cpu_time = multistart_variable_next_ascent_hillclimbing()
        else:
            print("Invalid choice.")
            sys.exit(1)

        print(f"Best Fitness: {fitness}")
        print(f"Evaluations: {evaluations}")
        print(f"CPU Time: {cpu_time:.4f} seconds")
        print("--------------------------")

def main():
    while True:
        print("Select CNF file:")
        print("1 - uf20-01.cnf")
        print("2 - uf100-01.cnf")
        print("3 - uf250-01.cnf")
        cnf_choice = input("Enter choice (1-3): ").strip()
        if cnf_choice not in CNF_FILES:
            print("Invalid CNF file choice.")
            continue

        cnf_path = CNF_FILES[cnf_choice]
        set_cnf_path(cnf_path)

        print("\nSelect Algorithm:")
        print("1 - Next Ascent Hillclimbing")
        print("2 - Multistart Next Ascent Hillclimbing")
        print("3 - Variable Neighbourhood Hillclimbing")
        print("4 - Multistart Variable Neighbourhood Hillclimbing")
        algo_choice = input("Enter choice (1-4): ").strip()
        if algo_choice not in ["1", "2", "3", "4"]:
            print("Invalid algorithm choice.")
            continue

        # ask for number of runs
        while True:
            try:
                num_runs = int(input("Enter number of runs: ").strip())
                if num_runs <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Please enter a valid positive integer.")

        run_algorithm(algo_choice, num_runs)

        again = input("\nDo you want to run another algorithm? (y/n): ").strip().lower()
        if again != 'y':
            print("Exiting...")
            break

if __name__ == "__main__":
    main()