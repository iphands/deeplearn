from agents                     import Learner
from environments.stupid_simple import Env
from models                     import StupidSimpleTestModel as Model
from collections                import deque
import numpy as np

env   = Env(done_steps = 100)
model = Model((1,), env.action_space.get_size())
agent = Learner(env, model)

for episode in range(0, 1000):
    env.reset()
    state = None
    score = 0

    state_buffer = deque(maxlen = 16)
    for i in range(0, 16):
        next_state, reward, done, info = env.step(0)
        state_buffer.append(next_state)

    while not env.done:
        # decide action
        action = agent.get_action(state)

        # perform action
        next_state, reward, done, info = env.step(action)
        state_buffer.append(next_state)
        next_state = np.reshape(state_buffer, [16, 1])

        # remember and store data
        # if not done:
        if not done and reward > 0:
            agent.remember(state, action, reward, next_state, done)

        score += reward
        state  = next_state

    print("Episode #{} Score: {}".format(episode, score))
    if score == 1000: break
    agent.train(256)
