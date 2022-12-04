import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import math
import numpy as np
import pygame
import argparse
import multiprocessing as mp
from neato import Ecosystem

import nogui_game2 as nogui_game


def fit_func(individual):
    """ Calculate the fitness of an individual. """
    food_score, time_score, death_score = [0, 0, 0]
    food_sum = 0
    for _ in range(0, 3):
        game = nogui_game.SnakeGame(200, individual, pygame)
        game.runGame()

        food_sum += game.score
        food_score += math.sqrt(math.pow(game.score, 3)) * 3000  # weigh picking up more food heavily
        time_score += (game.total_ticks / 10)  # use time in seconds as survival
        dist_to_food = math.sqrt(math.pow((game.snake_pos[0] - game.food_pos[0]), 2) + math.pow((game.snake_pos[1] - game.food_pos[1]), 2))
        death_score += (1 / dist_to_food) * 80000
    
    time_score /= 3.0
    death_score /= 3.0
    food_score /= 3.0
    if food_score <= 2000.0:
        food_score = death_score

    print('Foodscore: ' + str((food_sum)) + ' Fitness: ' + str(food_score + time_score))  # + avg_death_score
    
    return food_score + time_score  # + avg_death_score

parser = argparse.ArgumentParser()
parser.add_argument('--pop', nargs='?', type=int, default=25,
                    help='Specify the number of individuals in the population (default 25)')
parser.add_argument('--eliteism', action='store_true', help='Enables Eliteism')
parser.add_argument('--gens', nargs='?', type=int, default=100,
                    help='Specify the number of generations to train the population')
parser.add_argument('--mut_rate', nargs='?', type=float, default=0.5,
                    help='Specify how frequently a gene should randomly mutate')
parser.add_argument('--big_mut_rate', nargs='?', type=float, default=0.05,
                    help='Specify how frequently a gene should randomly mutate')
parser.add_argument('--cx_rate', nargs='?', type=float, default=0.1,
                    help='Specify how frequently a child should cross over')
parser.add_argument('--hidden_nodes', nargs='?', type=int, default=5, help='Specify how many hidden nodes to use')
parser.add_argument('--input_nodes', nargs='?', type=int, default=3, help='Specify how many input nodes')
parser.add_argument('--inputs', nargs='?', type=int, default=3,
                    help='Specify how many inputs will be fed to the input nodes')
parser.add_argument('--output_nodes', nargs='?', type=int, default=4, help='Specify how many output nodes')
parser.add_argument('--start_file', nargs='?', default='',
                    help='specify the file to get the starting population from (defualt generate random new pop)')
parser.add_argument('--disable_rate', nargs='?', type=float, default=0.001,
                    help='Specify how frequently a gene should be turned off')
parser.add_argument('--save_rate', nargs='?', type=int, default=5,
                    help='Specify how frequently to save the current generation to a file')

args = parser.parse_args()

input_count = args.inputs
output_node_count = args.output_nodes
input_node_count = args.input_nodes
hidden_node_count = args.hidden_nodes

pop_size = args.pop
genome_size = input_count * args.input_nodes + args.input_nodes * args.hidden_nodes + args.hidden_nodes * output_node_count
num_gens = args.gens

elitism = args.eliteism
mut_rate = args.mut_rate  # 2 / genome_size
big_mut_rate = args.big_mut_rate
cx_rate = args.cx_rate  # 1/2
disable_rate = args.disable_rate
save_rate = args.save_rate

if __name__ == '__main__':
    ecosystem = Ecosystem()
    ecosystem.create_initial_population(pop_size, input_size=input_count, output_size=output_node_count)
    for generation in range(0, num_gens):
        print("\n" + str(ecosystem))
        print("-" * 80 + " ")

        # test genomes and score fitness
        index = 0
        pool_args = [[genome] for genome in ecosystem.get_population()]
        pool = mp.Pool()
        fitnesses = pool.starmap(fit_func, pool_args)
        pool.close()
        for genome in ecosystem.get_population():
            genome.fitness = fitnesses[index]
            index += 1

        best_genome = ecosystem.get_best_genome()
        print(str(best_genome))
        print('best_fitness: ' + str(best_genome.fitness))

        # save genomes to file
        if generation % save_rate == 0:
            with open('generations\\gen' + str(generation) + '.txt', 'w') as f:
                f.write(str(pop_size))
                for genome in ecosystem.get_population():
                    f.write(str(genome))
                f.write(str(fitnesses))
            f.close()

        # crossover randomly from the top 50
        # if random.random() < cx_rate:
        #     killed = ecosystem.kill_percentage(30)
        #     print('killed ' + str(killed))
        #     for x in range(0, killed):
        #         parents = random.sample(ecosystem.get_population(), 2)
        #         ecosystem.add_genome(ecosystem.cross(parents[0], parents[1]))
        #     # ecosystem.next_generation(kill_percentage=0, mutate=True)
        # else:
        ecosystem.next_generation(kill_percentage=40, parent_genome=best_genome)

            # if generation < 400:
            #     if generation > 40 and generation % 10 == 0:
            #         ecosystem.next_generation(kill_percentage=50, parent_genome=best_genome)
            #     else:
            #         ecosystem.next_generation(kill_percentage=55)
            # else:
            #     ecosystem.next_generation(kill_percentage=50)
# python3 testneat.py --pop 100 --eliteism --gens 2 --mut_rate 0.005 --big_mut_rate 0.0002 --cx_rate 0.50 --hidden_nodes 20 --inputs 10 --input_nodes 5 --output_nodes 4 --disable_rate 0.0002 --save_rate 1