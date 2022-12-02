import copy
import itertools
import math
import random
import pygame
import argparse
import ast
import multiprocessing as mp

import nogui_game


def fit_func(individual, num_inputs, input_node_count, hidden_node_count, num_output_nodes):
    game1 = nogui_game.SnakeGame(120, individual, num_inputs, input_node_count, hidden_node_count, num_output_nodes, pygame)
    game1.runGame()

    """ Calculate the fitness of an individual. """

    #food_score = game1.score * 1000  # weigh picking up more food heavily
    #time_score = game1.total_ticks  # use time in seconds as survival
    food_score = math.sqrt(math.pow(game1.score, 3)) * 1400  # weigh picking up more food heavily

    time_score = (game1.total_ticks/10)  # use time in seconds as survival

    print('Foodscore: ' + str(game1.score) + ' Fitness: ' + str(food_score + time_score))
    return food_score + time_score


def tournament_selection(sample):
    scores = [sum(ind) for ind in sample]
    return sample[scores.index(max(scores))]


def random_selection(sample):
    return sample[random.randint(0, len(sample) - 1)]


def mutate_slightly(value):
    random_change = random.uniform(-0.1, 0.1)  # randomly mutates by -0.1 to 0.1

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
parser.add_argument('--big_mut_rate', nargs='?', type=float, default=0.05, help='Specify how frequently a gene should randomly mutate')
parser.add_argument('--cx_rate', nargs='?', type=float, default=0.1, help='Specify how frequently a child should cross over')
parser.add_argument('--hidden_nodes', nargs='?', type=int, default=5, help='Specify how many hidden nodes to use')
parser.add_argument('--input_nodes', nargs='?', type=int, default=3, help='Specify how many input nodes')
parser.add_argument('--inputs', nargs='?', type=int, default=3, help='Specify how many inputs will be fed to the input nodes')
parser.add_argument('--output_nodes', nargs='?', type=int, default=4, help='Specify how many output nodes')
parser.add_argument('--start_file', nargs='?', default='', help='specify the file to get the starting population from (defualt generate random new pop)')
parser.add_argument('--disable_rate', nargs='?', type=float, default=0.001, help='Specify how frequently a gene should be turned off')
parser.add_argument('--save_rate', nargs='?', type=int, default=5, help='Specify how frequently to save the current generation to a file')

args = parser.parse_args()
print(args.pop)
print(args.eliteism)
print(args.gens)
print(args.mut_rate)
print(args.cx_rate)
print(args.hidden_nodes)
print(args.input_nodes)

input_count = args.inputs
output_node_count = args.output_nodes

pop_size = args.pop
genome_size = input_count * args.input_nodes + args.input_nodes * args.hidden_nodes + args.hidden_nodes * output_node_count
num_gens = args.gens

elitism = args.eliteism
mut_rate = args.mut_rate #2 / genome_size
big_mut_rate = args.big_mut_rate
cx_rate = args.cx_rate  # 1/2
disable_rate = args.disable_rate

save_rate = args.save_rate
# For printing numbers at end to visualize.
max_fitnesses = []
avg_fitnesses = []
num_clones = []

population = []

# Initialize the population.
if args.start_file == '':
    for i in range(pop_size):
        population.append([random.uniform(-1.0, 1.0) for _ in range(genome_size)])
else:
    with open(args.start_file, 'r') as f:
        temp = int(f.readline())
        if pop_size <= temp:
            pop_size = temp
            for x in range(0, pop_size):
                population.append(ast.literal_eval(f.readline()))
        else:
            for x in range(temp):
                population.append(ast.literal_eval(f.readline()))
            for i in range(pop_size - temp):
                population.append([random.uniform(-1.0, 1.0) for _ in range(genome_size)])


    f.close()

# print(population)
if __name__ == '__main__':
    gen_count = 1
    for gen in range(num_gens):
        if gen_count == 150:
            mut_rate = mut_rate/3
            cx_rate = cx_rate*0.9
            big_mut_rate = big_mut_rate/4
            disable_rate = disable_rate/3

        print("\n" + "-" * 80 + " ")

        # Evaluate the population
        pool_args = [[p, input_count, args.input_nodes, args.hidden_nodes, output_node_count] for p in population]
        pool = mp.Pool()
        fitnesses = pool.starmap(fit_func, pool_args)
        pool.close()
        # fitnesses = [fit_func(p, input_count, args.input_nodes, args.hidden_nodes, output_node_count) for p in population]
        if (gen_count - 1) % save_rate == 0:
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
        # print("Max Fitness: {}".format(max_fitnesses[-1]))
        # print("Avg Fitness: {}".format(avg_fitnesses[-1]))

        # Print out the population.
        # Note: Comment out if you have larger populations as it might be hard to read.
        # print("Population Genomes:")
        # for p in population:
        #     print("\t\t\t", p)

        # Calculate duplicates
        duplicates = copy.deepcopy(population)
        duplicates.sort()

        # Track Number of Clones in Population
        num_clones.append(pop_size - len(list(k for k, _ in itertools.groupby(duplicates))))

        print("\tNumber of Clones in Population: {}".format(num_clones[-1]))
        # print("\tUnique Genomes in Population: ")
        # for clone in list(k for k, _ in itertools.groupby(duplicates)):
        #     print("\t\t\t\t", clone)

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
            par_1 = copy.deepcopy(tournament_selection(random.sample(population, 16)))
            par_2 = copy.deepcopy(tournament_selection(random.sample(population, 16)))

            # Perform crossover.
            new_ind = par_1[:]
            if random.random() < cx_rate:
                crossover_point = random.choice([0, genome_size])
                new_ind = par_1[:crossover_point] + par_2[crossover_point:]

            # Slightly mutate the individual.
            new_ind = [i if random.random() > mut_rate else (mutate_slightly(i)) for i in new_ind]

            # Mutate the individual.
            new_ind = [i if random.random() > big_mut_rate else random.uniform(-1.0, 1.0) for i in new_ind]

            # disable genes
            new_ind = [i if random.random() > disable_rate else 0 for i in new_ind]

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
