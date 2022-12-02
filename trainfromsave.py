import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy as np


# Set number of nodes for each layer, and dimensionality
inputs = 12
in_dim = (12,)
num_in_nodes = 17
in_hidden_dim = (17, 22)
num_hidden_nodes = 22
hidden_out_dim = (22, 4)
num_output_nodes = 4

# load the dataset
dataset = np.loadtxt('manualsave.csv', delimiter=',')
# split into input (X) and output (y) variables
X = dataset[:, 0:inputs]
y = dataset[:, inputs]

# Create the neural network model
model = Sequential()

# Add layers to the model
input_layer = model.add(Dense(num_in_nodes, input_shape=in_dim, activation="relu", name="Input"))
hidden_layer = model.add(Dense(num_hidden_nodes, activation="relu", name="Hidden"))
out_layer = model.add(Dense(num_output_nodes, activation="relu", name="Output"))

# Compiles the model, allows us to call it below
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X, y, epochs=1000, batch_size=20)
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))


def get_genome():
    # Get weights from neural network
    weights = model.get_weights()
    # Creates an array for genome, empty at start
    genome = np.array([], dtype=np.float32)
    # Skips the bias values from get_weights
    for x in range(0, len(weights), 2):
        # Append weights to genome copy, overwrite genome with new array
        genome = np.append(genome, weights[x])
    return genome


print(get_genome())

with open('manualgenome.txt', 'w') as f:
    gen = get_genome()
    for x in get_genome():
        f.write(str(x) + ', ')
f.close()
