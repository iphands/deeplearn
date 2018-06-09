#!/usr/bin/env python3

from pynput.keyboard import Key, Controller
import pynput.mouse as mouse
import time

timeout = 0.1
keyboard = Controller()

valid_controls = {
    'up':    'up',
    'down':  'down',
    'left':  'left',
    'right': 'right',
    'l':     'l',
    'r':     'r',
    'a':     'a',
    'b':     'b',
    'x':     'x',
    'y':     'y'
}

lst = []

for (k,v) in valid_controls.items():
    exec('def press_{}():   keyboard.press("{}")'.format(k, v))
    exec('def release_{}(): keyboard.release("{}")'.format(k, v))
    exec('lst.append(press_{})'.format(k))
    exec('lst.append(release_{})'.format(k))

def focus(geometry):
    print(geometry)
    mouse.Controller().position = (int(geometry['x'] + (geometry['w'] / 2)),
                                   int(geometry['y'] + (geometry['h'] / 2)))
    mouse.Controller().press(mouse.Button.left)
    time.sleep(0.100)
    mouse.Controller().release(mouse.Button.left)

def reset():
    keyboard.press('p')
    time.sleep(0.100)
    keyboard.release('p')

def get_inputs():
    return lst

if __name__ == '__main__':
    print(get_inputs())
