import sys
from agents            import Learner
from environments.kart import Env
from models            import KartModel

env   = Env(pid = sys.argv[1])
model = KartModel(env.get_input_shape(), env.get_action_size())
agent = Learner(env, model)

for episode in range(0, 1000):
    env.reset()
    state = None
    score = 0

    while not env.done:
        # decide action
        action = agent.get_action(state)

        # perform action
        next_state, reward, done, info = env.step(action)

        # remember and store data
        # if not done
        if not done and reward > 0:
            agent.remember(state, action, reward, next_state, done)

        score += reward
        state  = next_state

    print("Episode #{} Score: {}".format(episode, score))
    agent.train(128)
