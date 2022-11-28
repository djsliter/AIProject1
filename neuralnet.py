from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy as np


class NeuralNetwork:
    def __init__(self, in_dim, num_in_nodes, in_hidden_dim, num_hidden_nodes, hidden_out_dim, num_output_nodes):
        # Set number of nodes for each layer, and dimensionality
        self.in_dim = (3,)  # TODO swap for vals in constructor
        self.num_in_nodes = 3
        self.in_hidden_dim = (3, 5)
        self.num_hidden_nodes = 5
        self.hidden_out_dim = (5, 4)
        self.num_output_nodes = 4

        # Create the neural network model
        self.model = Sequential()

        # Add layers to the model
        self.input_layer = self.model.add(Dense(num_in_nodes, input_shape=in_dim, activation="relu", name="Input"))
        self.hidden_layer = self.model.add(Dense(num_hidden_nodes, activation="relu", name="Hidden"))
        self.out_layer = self.model.add(Dense(num_output_nodes, activation="relu", name="Output"))

        # Compiles the model, allows us to call it below
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    def get_genome(self):
        # Get weights from neural network
        weights = self.model.get_weights()
        # Creates an array for genome, empty at start
        genome = np.array([], dtype=np.float32)
        # Skips the bias values from get_weights
        for x in range(0, len(weights), 2):
            # Append weights to genome copy, overwrite genome with new array
            genome = np.append(genome, weights[x])
        return genome

    def set_weights_from_genome(self, genome):
        # Implement function that takes in the genome, then sets weights of the net
        # properly in accordance with the provided 1D array. Tricky, requires
        # reshaping segments of the genome array, setting bias values to 0, etc.
        # Format for model.set_weights(wts) =
        wts = [
            np.array([[genome[0], genome[1], genome[2]], [genome[3], genome[4], genome[5]],
                      [genome[6], genome[7], genome[8]]], dtype=np.float32),
            np.array([0., 0., 0.], dtype=np.float32),
            np.array([[genome[9], genome[10], genome[11], genome[12], genome[13]],
                       [genome[14], genome[15], genome[16], genome[17], genome[18]],
                      [genome[19], genome[20], genome[21], genome[22], genome[23]]], dtype=np.float32),
            np.array([0., 0., 0., 0., 0.], dtype=np.float32),
            np.array([[genome[24], genome[25], genome[26], genome[27]],
                       [genome[28], genome[29], genome[30], genome[31]],
                      [genome[32], genome[33], genome[34], genome[35]],
                      [genome[36], genome[37], genome[38], genome[39]],
                      [genome[40], genome[41], genome[42], genome[43]]], dtype=np.float32),
            np.array([0., 0., 0., 0.], dtype=np.float32)
        ]
        # Need to build the shape of wts above from provided genome
        self.model.set_weights(wts)

        # Runs data through model as a function
    def runModel(self, data):
        # Runs our data through the model
        q = self.model(data)
        # Sets action to the output node index with highest value
        action = np.argmax(q)
        print("ACTION VALUE: ", q[0][action], "\nACTION: ", action)
        return action
