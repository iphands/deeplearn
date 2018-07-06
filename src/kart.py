import sys
import time
import numpy as np

from agents            import Learner
from environments.kart import Env
from models            import KartModel
from collections       import deque

env   = Env(pid = sys.argv[1])
model = KartModel(env.get_input_shape(), env.get_action_size())
agent = Learner(env, model)

steps = 4

for episode in range(0, 1000):
    env.reset()
    state = None
    score = 0

    state_buffer = deque(maxlen = steps)
    for i in range(0, steps):
        next_state, reward, done, info = env.step(0)
        state_buffer.append(next_state)


    i = 0
    while not env.done:
        t = time.time()

        # decide action
        action = agent.get_action(state)

        # perform action
        next_state, reward, done, info = env.step(action)
        state_buffer.append(next_state)
        next_state = np.array(state_buffer)

        # remember and store data
        if not done:
            agent.remember(state, action, reward, next_state, done)

        score += reward
        state  = next_state

        # close to const delay
        e = (time.time() - t)
        sleep = (0.01666 - e)
        if sleep > 0:
            time.sleep(sleep)
        else:
            print("No skip! {}".format(e))
        i += 1

    print("Episode #{} Score: {} Ticks {}".format(episode, score, i))
    agent.train(1024)
