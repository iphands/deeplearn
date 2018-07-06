import numpy  as np
import random

from collections  import deque

class Learner():
    def __init__(self, env, model):
        self.model             = model
        self.env               = env

        self.gamma             = 0.95
        self.exploration_rate  = 0.75
        self.exploration_min   = 0.01
        self.exploration_decay = 0.25

        self.memory            = deque(maxlen = (1024*1024))

    def get_action(self, state):
        if state is None: return # skip if this is the first

        if np.random.rand() <= self.exploration_rate:
            # take a random action
            return self.env.action_space.sample()

        # reshape the screen state input
        state = self.model.reshape(state)

        # decide on an action to take
        return np.argmax(self.model.instance.predict(state)[0])

    def train(self, sample_size):
        if (len(self.memory) < sample_size):
            # Not enough samples in our memory to train on
            return

        samples = random.sample(self.memory, sample_size)

        for state, action, reward, next_state, done in samples:
            target = reward
            if not done:
                next_state = self.model.reshape(next_state)
                target = reward + self.gamma * np.amax(self.model.instance.predict(next_state)[0])

            state = self.model.reshape(state)
            target_f = self.model.instance.predict(state)
            target_f[0][action] = target
            self.model.instance.fit(state, target_f, epochs=1, verbose=0)

        if self.exploration_rate > self.exploration_min:
            self.exploration_rate *= self.exploration_decay

    def remember(self, state, action, reward, next_state, done):
        if state is None: return # skip if this is the first

        # append the step output as a tuple to our memory
        self.memory.append((state, action, reward, next_state, done))
