import numpy as np
import neurolab as nl

# Make neural network, get all weights into list/array
# Inputs: food position, snake head pos, snake tail pos
# foodX, foodY, headX, headY, tailX, tailY
# Outputs: left, right, up, down

input = np.random.uniform(-0.5, 0.5, (10, 3))
target = (input[:, 0] + input[:, 1] + input[:, 2]).reshape(10, 1)
# Create network with 2 inputs, 5 neurons in input layer and 1 in output layer
net = nl.net.newff([[-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5]], [8, 1])
# Train process
net.trainf = nl.train.train_gd
err_progress = net.train(input, target, epochs= 40000, show=2000, goal=0.001)
# print(err_progress)
# Compute average from 100 runs
i = 0
avg = 0
while i < 1000:
    avg += net.sim([[0.1, 0.4, 0.5]])[0][0] # x + y + z
    i+= 1
print("RESULT ------------- ", avg/i)

# i= 0
# while i < len(net.layers):
#     print("W", i, ": ", net.layers[i].np['w'])
#     i+=1

# [0.45, 0.2, 0.35]

# Input        Hidden          Output
#                 1
#                 1
#                 1
# 0.45            1
#                 1
#                 1             1 => 
# 0.2             1
#                 1
# 0.35            1
#                 1
#                 1