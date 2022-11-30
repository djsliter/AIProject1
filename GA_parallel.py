import copy
import itertools
import random
import pygame
import argparse
import ast
import multiprocessing as mp

import nogui_game

def fit_func(individual, num_inputs=5, input_node_count=6, hidden_node_count=10, num_output_nodes=4):
    game1 = nogui_game.SnakeGame(120, individual)
    game1.runGame()

    """ Calculate the fitness of an individual. """

    food_score = game1.score * 1000  # weigh picking up more food heavily
    time_score = game1.total_ticks  # use time in seconds as survival time
    print(food_score + time_score)
    return food_score + time_score

def tournament_selection(sample):
    scores = [sum(ind) for ind in sample]
    return sample[scores.index(max(scores))]


def random_selection(sample):
    return sample[random.randint(0, len(sample) - 1)]


def mutate_slightly(value):
    random_val = random.random()
    random_sign = -1 if random.random() <= 0.5 else 1
    random_change = random_val * random_sign * 0.1  # randomly mutates by -0.1 to 0.1

    new_weight = value + random_change
    if new_weight <= -1.0:  # keep weights above -1
        return -1.0
    elif new_weight >= 1.0:  # keep weights below 1
        return 1.0
    else:
        return new_weight

# note: can't specify number of inputs (not input nodes) because NN constructor uses inputs as args
parser = argparse.ArgumentParser()
parser.add_argument('--pop', nargs='?', type=int, default=25, help='Specify the number of individuals in the population (default 25)')
parser.add_argument('--eliteism', action='store_true', help='Enables Eliteism')
parser.add_argument('--gens', nargs='?', type=int, default=100, help='Specify the number of generations to train the population')
parser.add_argument('--mut_rate', nargs='?', type=float, default=0.5, help='Specify how frequently a gene should randomly mutate')
parser.add_argument('--cx_rate', nargs='?', type=float, default=0.1, help='Specify how frequently a child should cross over')
parser.add_argument('--hidden_nodes', nargs='?', type=int, default=5, help='Specify how many hidden nodes to use')
parser.add_argument('--input_nodes', nargs='?', type=int, default=3, help='Specify how many input nodes')
parser.add_argument('--start_file', nargs='?', default='', help='specify the file to get the starting population from (defualt generate random new pop)')


args = parser.parse_args()
print(args.pop)
print(args.eliteism)
print(args.gens)
print(args.mut_rate)
print(args.cx_rate)
print(args.hidden_nodes)
print(args.input_nodes)

input_count = 3
output_node_count = 4

pop_size = args.pop
genome_size = input_count * args.input_nodes + args.input_nodes * args.hidden_nodes + args.hidden_nodes * output_node_count
num_gens = args.gens

elitism = args.eliteism
mut_rate = args.mut_rate #2 / genome_size
cx_rate = args.cx_rate  # 1/2


# For printing numbers at end to visualize.
max_fitnesses = []
avg_fitnesses = []
num_clones = []

population = []

# Initialize the population.
if args.start_file == '':
    for i in range(pop_size):
        population.append([random.random() if random.random() >= 0.6 else -random.random() for _ in range(genome_size)])
else:
    with open(args.start_file, 'r') as f:
        pop_size = int(f.readline())
        for x in range(0, pop_size):
            population.append(ast.literal_eval(f.readline()))
    f.close()


if __name__ == '__main__':
    
    gen_count = 1
    for gen in range(num_gens):

        print("\n" + "-" * 80 + " ")
        # Multiprocess logic
        pool_args = [[p] for p in population]
        pool = mp.Pool()
        fitnesses = pool.starmap(fit_func, pool_args)
        pool.close()

        with open('generations\\gen' + str(gen_count) + '.txt', 'w') as f:
            f.write(str(pop_size) + '\n')
            for p in population:
                f.write(str(p) + '\n')
            f.write(str(fitnesses) + '\n')
        f.close()
        gen_count += 1
        # Track fitnesses
        max_fitnesses.append(max(fitnesses))
        avg_fitnesses.append(sum(fitnesses) / len(fitnesses))

        print("Generation: {}".format(gen), end=" ")
        print("Max Fitness: {}".format(max_fitnesses[-1]))
        print("Avg Fitness: {}".format(avg_fitnesses[-1]))

        # Print out the population.
        # Note: Comment out if you have larger populations as it might be hard to read.
        print("Population Genomes:")
        for p in population:
            print("\t\t\t", p)

        # Calculate duplicates
        duplicates = copy.deepcopy(population)
        duplicates.sort()

        # Track Number of Clones in Population
        num_clones.append(pop_size - len(list(k for k, _ in itertools.groupby(duplicates))))

        print("\tNumber of Clones in Population: {}".format(num_clones[-1]))
        print("\tUnique Genomes in Population: ")
        for clone in list(k for k, _ in itertools.groupby(duplicates)):
            print("\t\t\t\t", clone)

        # Early Exit
        # if max(fitnesses) == genome_size:
        # 	break

        new_pop = []

        # Elitism
        if elitism:
            print("Keeping Elite Individual")
            new_pop.append(copy.deepcopy(population[fitnesses.index(max(fitnesses))]))

        for _ in range(pop_size - len(new_pop)):

            # Select two parents.
            par_1 = copy.deepcopy(tournament_selection(random.sample(population, 3)))
            par_2 = copy.deepcopy(tournament_selection(random.sample(population, 3)))

            # Perform crossover.
            new_ind = par_1[:]
            if random.random() < cx_rate:
                crossover_point = random.choice([0, genome_size])
                new_ind = par_1[:crossover_point] + par_2[crossover_point:]

            # Mutate the individual.
            new_ind = [i if random.random() > mut_rate else (mutate_slightly(i)) for i in new_ind]

            # Add to the population
            new_pop.append(new_ind)

        population = new_pop

# Print out final population
# print("\n\n\nFinal Population is:")
# for p in population:
#     print(f"Fitness: {fit_func(p)}, Individual: {p}")

# Print out final tracking information.
print()
print("gens = " + str([g for g in range(num_gens)]))
print("max_fit = " + str(max_fitnesses))
print("avg_fit = " + str(avg_fitnesses))
print("num_clones = " + str(num_clones))
