import math

import pygame, sys, time, random
import neuralnet as nn
import numpy as np

class SnakeGame:
    def __init__(self, difficulty, genome, input_count=5, input_node_count=6, hidden_node_count=10, output_node_count=4, pygame=pygame):
        self.input_count = input_count
        self.input_node_count = input_node_count
        self.hidden_node_count = hidden_node_count
        self.output_node_count = output_node_count
        # Difficulty settings
        # Easy      ->  10
        # Medium    ->  25
        # Hard      ->  40
        # Harder    ->  60
        # Impossible->  120
        self.difficulty = difficulty
        self.genome = genome
        # Window size
        self.frame_size_x = 720
        self.frame_size_y = 480

        self.total_ticks = 0
        # Checks for errors encountered
        check_errors = pygame.init()
        # pygame.init() example output -> (6, 0)
        # second number in tuple gives number of errors
        if check_errors[1] > 0:
            print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
            sys.exit(-1)
        # else:
        #     print('[+] Game successfully initialised')
        
        # Colors (R, G, B)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        self.magenta = pygame.Color(255, 0, 255)

        # FPS (frames per second) controller
        self.fps_controller = pygame.time.Clock()

        # Game variables
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

        self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
        self.food_spawn = True

        self.direction = 'RIGHT'
        self.change_to = self.direction

        self.score = 0
        self.pygame = pygame

    # Game Over
    def game_over(self):
        self.pygame.quit()
        #sys.exit()

    def runGame(self):
        # Initialise game window
        
        neural_net = nn.NeuralNetwork((self.input_count, ), self.input_node_count, (self.input_node_count, self.hidden_node_count), self.hidden_node_count, (self.hidden_node_count, self.output_node_count), self.output_node_count)
        neural_net.set_weights_from_genome(self.genome)
        self.last_choice = 0
        self.last_eat_time = 0
        # Main logic
        while True:
            distance_from_head_x_to_food_x = (self.snake_pos[0] - self.food_pos[0]) / self.frame_size_x # math.sqrt(math.pow((self.snake_pos[0] - self.food_pos[0]), 2))
            distance_from_head_y_to_food_y = (self.snake_pos[1] - self.food_pos[1]) / self.frame_size_y # math.sqrt(math.pow((self.snake_pos[1] - self.food_pos[1]), 2))
            distance_from_head_x_to_tail_x = (self.snake_pos[0] - self.snake_body[len(self.snake_body) - 1][0])/ self.frame_size_x
            distance_from_head_y_to_tail_y = (self.snake_pos[1] - self.snake_body[len(self.snake_body) - 1][1])/ self.frame_size_y
            direction_x = 0
            direction_y = 0
            left_safe = 0
            right_safe = 0
            down_safe = 0
            up_safe = 0
            if self.direction == 'UP':
                direction_x = 0
                direction_y = -1
            if self.direction == 'DOWN':
                direction_x = 0
                direction_y = 1
            if self.direction == 'LEFT':
                direction_x = -1
                direction_y = 0
            if self.direction == 'RIGHT':
                direction_x = 1
                direction_y = 0

            up_pos = self.snake_pos[1] - 10
            if up_pos < 0 or [self.snake_pos[0], up_pos] in self.snake_body:
                up_safe = -1
            else:
                up_safe = 1
            right_pos = self.snake_pos[0] + 10
            if right_pos > self.frame_size_y or [right_pos, self.snake_pos[1]] in self.snake_body:
                right_safe = -1
            else:
                right_safe = 1
            left_pos = self.snake_pos[0] - 10
            if left_pos < 0 or [left_pos, self.snake_pos[1]] in self.snake_body:
                left_safe = -1
            else:
                left_safe = 1
            down_pos = self.snake_pos[1] + 10
            if down_pos > self.frame_size_y or [self.snake_pos[0], down_pos] in self.snake_body:
                down_safe = -1
            else:
                down_safe = 1

            # Neural net makes a choice
            choice = neural_net.runModel(np.array([[distance_from_head_x_to_food_x, distance_from_head_y_to_food_y, distance_from_head_x_to_tail_x, distance_from_head_y_to_tail_y, self.last_choice, direction_x, direction_y, up_safe, down_safe, left_safe, right_safe]], dtype=np.float32))
            self.last_choice = choice
            # Based on choice, set direction to change to
            if choice == 0 and self.direction != 'DOWN':
                self.change_to = 'UP'
            if choice == 1 and self.direction != 'LEFT':
                self.change_to = 'RIGHT'
            if choice == 2 and self.direction != 'UP':
                self.change_to = 'DOWN'
            if choice == 3 and self.direction != 'RIGHT':
                self.change_to = 'LEFT'
            # Making sure the snake cannot move in the opposite self.direction instantaneously
            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

            # Moving the snake
            if self.direction == 'UP':
                self.snake_pos[1] -= 10
            if self.direction == 'DOWN':
                self.snake_pos[1] += 10
            if self.direction == 'LEFT':
                self.snake_pos[0] -= 10
            if self.direction == 'RIGHT':
                self.snake_pos[0] += 10

            # Snake body growing mechanism
            self.snake_body.insert(0, list(self.snake_pos))
            if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
                self.score += 1
                self.food_spawn = False
                self.last_eat_time = self.total_ticks
            else:
                self.snake_body.pop()

            # Spawning food on the screen
            if not self.food_spawn:
                self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
            self.food_spawn = True

            
            # Game Over conditions -----------------------------------------------
            if self.total_ticks > self.last_eat_time + 100000:
                self.game_over()
                # print('total_ticks ' + str(self.total_ticks))
                # print('score ' + str(self.score))
                break
            # Getting out of bounds
            if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-10:
                self.game_over()
                # print('total_ticks ' + str(self.total_ticks))
                # print('score ' + str(self.score))
                break
            if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-10:
                self.game_over()
                # print('total_ticks ' + str(self.total_ticks))
                # print('score ' + str(self.score))
                break
            # Touching the snake body
            for block in self.snake_body[1:]:
                if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                    self.game_over()
                    # print('total_ticks ' + str(self.total_ticks))
                    # print('score ' + str(self.score))
                    break
            # Refresh rate
            self.fps_controller.tick(self.difficulty)
            self.total_ticks += self.difficulty