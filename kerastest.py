from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy as np

# Create the neural network model
model = Sequential()
# Add layers to the model
layer_a = model.add(Dense(3, input_shape=(3, ), activation="relu"))

out_layer = model.add(Dense(1, activation="relu"))
model.set_weights([
    np.array([[0.3, 0.1, 0.4], [0.3, 0.1, 0.4], [0.3, 0.1, 0.4]], dtype=np.float32), 
    np.array([0., 0., 0.], dtype=np.float32), 
    np.array([[0.3], [0.1], [0.4]], dtype=np.float32), 
    np.array([0.], dtype=np.float32)
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

data = [[0.1, 0.4, 0.5],[0.4, 0.3, 0.6],[0.2, 0.4, 0.4]]
model.evaluate(data,  [[1], [1], [1]])

print(model.get_weights())


# 1        1
# 1        1       1
# 1        1   