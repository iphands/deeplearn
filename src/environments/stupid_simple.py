import random
import numpy  as np

class ActionSpace():
    def __init__(self, lst):
        self.lst = lst

    def get_size(self):
        return len(self.lst)

    def sample(self):
        return random.sample(self.lst, 1)[0]

class Env():
    def __init__(self, done_steps = 100):
        self.done_counter = 0
        self.max_steps    = done_steps
        self.done         = False
        self.action_space = ActionSpace(range(0, 512))

    def reset(self):
        self.done = False
        self.done_counter = 0

    def get_done(self):
        self.done_counter += 1
        if self.done_counter > self.max_steps: self.done = True
        return self.done

    def render(self):
        pass

    def step(self, action):
        self.get_done()
        observation = np.array([int(random.random() * 10)])
        reward      = 10 if (action == 1) else 0
        done        = self.done
        info        = None
        return (observation, reward, done, info)
