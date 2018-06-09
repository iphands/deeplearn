# Python

import tensorflow as tf
import screengrab as sg
import json
import utils as utils
import re

sg.init()
window = utils.find_window('.*MARIO.*')
hier   = utils.get_hier(window)

geometry = utils.get_geometry(hier[2])

# remove kwin window decoration
geometry_relative =  utils.get_geometry(hier[1])
geometry['x'] += geometry_relative['x']
geometry['y'] += geometry_relative['y']
geometry['w'] = geometry_relative['w']
geometry['h'] = geometry_relative['h']

im = sg.grab_screen_grey(geometry['x'], geometry['y'], geometry['w'], geometry['h'])
im.save('./output/test.png', 'PNG')
sg.destroy()
