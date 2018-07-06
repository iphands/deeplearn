import numpy  as np
import random

from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D

class KartModel():
    def __init__(self, input_shape, action_size):
        model = Sequential()

        # Convolutional layers
        model.add(Conv2D(32, 8, strides=(4, 4), padding='valid', activation='relu', input_shape=input_shape))
        model.add(Conv2D(64, 4, strides=(2, 2), padding='valid', activation='relu', input_shape=input_shape))
        model.add(Conv2D(64, 3, strides=(1, 1), padding='valid', activation='relu', input_shape=input_shape))

        # Flatten the convolution output
        model.add(Flatten())

        # First dense layer
        model.add(Dense(512, activation='relu'))

        # Output layer
        model.add(Dense(action_size, activation='linear'))
        model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['accuracy'])
        self.instance = model

    def reshape(self, data):
        return np.array([data])

class StupidSimpleTestModel():
    def __init__(self, input_shape, action_size):
        model = Sequential()
        model.add(Dense(16, input_shape=(1,), activation='relu'))
        model.add(Dense(action_size, activation='linear'))
        model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['accuracy'])
        model.reshape = self.reshape
        self.instance = model

    def reshape(self, data):
        return data
