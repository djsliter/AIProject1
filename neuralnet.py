from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy as np

# Set number of nodes for each layer, and dimensionality
in_dim = (3, )
num_in_nodes = 3
in_hidden_dim = (3, 5)
num_hidden_nodes = 5
hidden_out_dim = (5, 4)
num_output_nodes = 4

# Create the neural network model
model = Sequential()
# Add layers to the model
input_layer = model.add(Dense(num_in_nodes, input_shape=in_dim,activation="relu", name="Input"))
hidden_layer = model.add(Dense(num_hidden_nodes, activation="relu", name="Hidden"))
out_layer = model.add(Dense(num_output_nodes, activation="relu", name="Output"))

# Compiles the model, allows us to call it below
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

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

def set_weights_from_genome(genome):
    # Implement function that takes in the genome, then sets weights of the net
    # properly in accordance with the provided 1D array. Tricky, requires
    # reshaping segments of the genome array, setting bias values to 0, etc.
    # Format for model.set_weights(wts) = 
    wts = [
        np.array([[0.3, 0.1, 0.4],[0.3, 0.1, 0.4],[0.3, 0.1, 0.4]], dtype=np.float32), 
        np.array([0., 0., 0.], dtype=np.float32),
        np.array([[0.3, 0.3, 0.1, 0.4, 0.57], [0.1, 0.3, 0.1, 0.4, 0.57], [0.4, 0.3, 0.1, 0.4, 0.57]], dtype=np.float32), 
        np.array([0., 0., 0., 0., 0.], dtype=np.float32), 
        np.array([[0.3, 0.64, 0.4, 0.9],
                [0.3, 0.1, 0.4, 0.9],
                [0.3, 0.1, 0.4, 0.9],
                [0.25, 0.1, 0.4, 0.9],
                [0.3, 0.7, 0.4, 0.9]], dtype=np.float32), 
        np.array([0., 0., 0., 0.], dtype=np.float32)
    ]
    # Need to build the shape of wts above from provided genome
    return genome

# Runs data through model as a function
def runModel(data):
    # Runs our data through the model
    q = model(data)
    # Sets action to the output node index with highest value
    action = np.argmax(q)
    print("ACTION VALUE: ", q[0][action], "\nACTION: ", action)
    return action