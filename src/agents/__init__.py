import numpy  as np
import random

from collections  import deque
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D

class Learner():
    def __init__(self, env):
        self.env               = env
        self.gamma             = 0.95
        self.action_size       = env.action_space.get_size()
        self.example_screen    = self.env.get_screen()
        self.model             = self._build_model()
        self.memory            = deque(maxlen = (1024*1024))
        self.exploration_rate  = 0.5
        self.exploration_min   = 0.01
        self.exploration_decay = 0.25


    def _build_model(self):
        model = Sequential()

        # Convolutional layers
        model.add(Conv2D(32, 8, strides=(4, 4), padding='valid', activation='relu', input_shape=self.example_screen.shape))
        model.add(Conv2D(64, 4, strides=(2, 2), padding='valid', activation='relu', input_shape=self.example_screen.shape))
        model.add(Conv2D(64, 3, strides=(1, 1), padding='valid', activation='relu', input_shape=self.example_screen.shape))

        # Flatten the convolution output
        model.add(Flatten())

        # First dense layer
        model.add(Dense(512, activation='relu'))

        # Output layer
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['accuracy'])
        return model


    def _build_model_old(self):
        model = Sequential()
        model.add(Dense(16, input_shape=(1,), activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['accuracy'])
        return model

    def get_action(self, state):
        if state is None: return # skip if this is the first

        if np.random.rand() <= self.exploration_rate:
            # take a random action
            return self.env.action_space.sample()

        # reshape the screen state input
        state = np.array([state])

        # decide on an action to take
        return np.argmax(self.model.predict(state)[0])

    def train(self, sample_size):
        if (len(self.memory) < sample_size):
            # Not enough samples in our memory to train on
            return

        samples = random.sample(self.memory, sample_size)

        for state, action, reward, next_state, done in samples:
            target = reward
            if not done:
                next_state = np.array([next_state])
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])

            state = np.array([state])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.exploration_rate > self.exploration_min:
            self.exploration_rate *= self.exploration_decay

    def remember(self, state, action, reward, next_state, done):
        if state is None: return # skip if this is the first

        # append the step output as a tuple to our memory
        self.memory.append((state, action, reward, next_state, done))
