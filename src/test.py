# Python

import tensorflow as tf
import screengrab as sg
import readmem    as rm
import json
import utils as utils
import re
import sys
import time
import timeit

sg.init()
window   = utils.find_window('.*Mkart.*')
hier     = utils.get_hier(window)
geometry = utils.get_geometry(hier[2])

# remove kwin window decoration
geometry_relative =  utils.get_geometry(hier[1])
geometry['x'] += geometry_relative['x']
geometry['y'] += geometry_relative['y']
geometry['w'] = geometry_relative['w']
geometry['h'] = geometry_relative['h']

# im = sg.grab_screen_grey(geometry['x'], geometry['y'], geometry['w'], geometry['h'])
# im.save('./output/test.png', 'PNG')
# sg.destroy()

pid = int(sys.argv[1])
heap_start = None

with open('/proc/{}/maps'.format(pid)) as f:
    for line in  f.readlines():
        if '[heap]' in line:
            heap_start = line.split('-')[0]
            heap_start = int(heap_start, 16)

previous_rank = None

rank = rm.get_player_rank(pid, heap_start)
# while True:
#     rank = rm.get_player_rank(pid, heap_start)
#     print('Current rank is: {}'.format(rank))
#     if rank != previous_rank and rank > 0 and rank < 9:
#         print('Current rank is: {}'.format(rank))
#     previous_rank = rank
#     time.sleep(0.01)



