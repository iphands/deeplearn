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
    def __init__(self, done_steps = 100, pid = None):
        self.pid          = pid
        self.done_counter = 0
        self.max_steps    = done_steps
        self.done         = False
        self.action_space = ActionSpace(range(0, 4))

    def _start_kart(self):
        input_wrapper.reset()

        sg.init()
        window   = utils.find_window('.*Mkart.*')
        hier     = utils.get_hier(window)
        geometry = utils.get_geometry(hier[1])

        # tweak for half screen view and kill menubar
        geometry['y'] += 30
        geometry['h']  = 105
        geometry['w'] -= 5

        im = sg.grab_screen_grey(geometry['x'], geometry['y'], geometry['w'], geometry['h'])
        im = sg.get_image_grey(geometry['w'], geometry['h'], im)
        im.save('./output/test.png', 'PNG')

        pid = self.pid
        heap_start = None

    def reset(self):
        self.done = False
        self.done_counter = 0

    def get_done(self):
        return self.get_rank() == 8

    def set_rank(self):
        rank = rm.get_player_rank(pid, heap_start)
        if rank > 0 and rank < 9:
            self.rank = rank
            return
        time.sleep(0.033) # sleep for one frame
        return

    def get_reward(self, rank, previous_rank):
        if rank == previous_rank:
            return 4 - rank
        if rank < previous_rank:
            return 10
        if rank > previous_rank:
            return -10

    def step(self, action):
        self.set_done()
        self.set_rank()

        observation = np.array([int(random.random() * 10)])
        reward      = get_reward(self.rank, self.previous_rank)
        done        = self.done
        info        = None
        return (observation, reward, done, info)
