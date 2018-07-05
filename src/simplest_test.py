from agents                     import Learner
# from environments.stupid_simple import Env
from environments.kart import Env

env   = Env(done_steps = 100)
agent = Learner(env)

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