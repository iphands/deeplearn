#!/usr/bin/env python3

from pynput.keyboard import Key, Controller
import pynput.mouse as mouse
import time

timeout = 0.1
keyboard = Controller()

valid_keys = {
    # 'up':    'up',
    # 'down':  'down',
    'left':  'left',
    'right': 'right',
}

valid_chars = {
    #'l':     False,
    #'a':     False,
    'b':     False,
    # 'y':     'y'
}

lst = []
release_lst = []

for (k,v) in valid_chars.items():
    exec('def press_{}():   valid_chars["{}"] = True  ; keyboard.press("{}")'.format(k, k, k))
    exec('def release_{}(): valid_chars["{}"] = False ; keyboard.release("{}")'.format(k, k, k))
    exec('lst.append(press_{})'.format(k))
    exec('lst.append(release_{})'.format(k))
    exec('release_lst.append(release_{})'.format(k))

for (k,v) in valid_keys.items():
    exec('def press_{}():   keyboard.press(Key.{})'.format(k, v))
    exec('def release_{}(): keyboard.release(Key.{})'.format(k, v))
    exec('lst.append(press_{})'.format(k))
    exec('lst.append(release_{})'.format(k))
    exec('release_lst.append(release_{})'.format(k))

def focus(geometry):
    mouse.Controller().position = (int(geometry['x'] + (geometry['w'] / 2)), int(geometry['y'] + (geometry['h'] / 2)))
    mouse.Controller().press(mouse.Button.left)
    time.sleep(0.100)
    mouse.Controller().release(mouse.Button.left)

def get_pressed():
    pressed = {}
    for (k,v) in valid_chars.items():
        if (v):
            pressed[k] = True
    return pressed

def get_keyboard():
    return keyboard

def release():
    for f in lst:
        f()
        time.sleep(0.100)

def reset():
    keyboard.press('p')
    time.sleep(0.100)
    keyboard.release('p')

def get_input_count():
    return len(lst)

def do_input(num):
    lst[num]()

if __name__ == '__main__':
    print(get_inputs())
