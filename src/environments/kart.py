import random
import numpy      as np
import screengrab as sg
import readmem    as rm
import inputs     as input_wrapper
import utils      as utils
import time

class ActionSpace():
    def __init__(self):
        self.size = input_wrapper.get_input_count()

    def get_size(self):
        return self.size

    def sample(self):
        return np.random.randint(0, self.size)

class Env():
    def __init__(self, done_steps = 100, pid = None):
        self.pid          = int(pid)
        self.done_counter = 0
        self.max_steps    = done_steps
        self.done         = False
        self.rank         = 5
        self.action_space = ActionSpace()

        # start the stuff
        self._start_kart()

        self.set_rank()
        self.rank          = None
        self.previous_rank = self.rank

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

        self.geometry = geometry

        im = sg.grab_screen_grey(geometry['x'], geometry['y'], geometry['w'], geometry['h'])
        im = sg.get_image_grey(geometry['w'], geometry['h'], im)
        im.save('./output/test.png', 'PNG')

        with open('/proc/{}/maps'.format(self.pid)) as f:
            for line in  f.readlines():
                if '[heap]' in line:
                    heap_start      = line.split('-')[0]
                    heap_start      = int(heap_start, 16)

                    self.heap_start = heap_start
                    break

    def reset(self):
        self.done = False
        input_wrapper.reset()

    def get_done(self):
        return self.get_rank() == 8

    def set_rank(self):
        self.previous_rank = self.rank
        rank = rm.get_player_rank(self.pid, self.heap_start)
        if rank > 0 and rank < 9:
            self.rank = rank
            return
        time.sleep(0.033) # sleep for one frame
        return

    def set_done(self):
        self.done = self.rank == 8

    def get_position_reward(self, rank, previous_rank):
        if not rank or not previous_rank: return 0

        if rank == previous_rank:
            return 1
        if rank < previous_rank:
            return 10
        if rank > previous_rank:
            return -100

    def get_reward(self, rank, previous_rank):
        b_mod = 0

        if 'b' in input_wrapper.get_pressed():
            # give extra points for mashing B
            b_mod = 1

        return b_mod + self.get_position_reward(rank, previous_rank)

    def get_pixel_data(self):
        return sg.grab_screen_grey(
            self.geometry['x'],
            self.geometry['y'],
            self.geometry['w'],
            self.geometry['h'])

    def get_screen(self):
        return np.reshape(self.get_pixel_data(), [self.geometry['w'], self.geometry['h'], 1])

    def do_action(self, action):
        input_wrapper.do_input(action)

    def step(self, action):
        if action is not None: self.do_action(action)
        self.set_rank()
        self.set_done()

        observation = self.get_screen()
        reward      = self.get_reward(self.rank, self.previous_rank)
        done        = self.done
        info        = None

        return (observation, reward, done, info)
