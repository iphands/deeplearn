#!/usr/bin/env python3
import ctypes
import os
import sys
from PIL import Image

screen = ctypes.CDLL(os.path.dirname(os.path.realpath(__file__)) + '/screen.so')

def init():
    screen.init()

def destroy():
    screen.destroy()

def grab_screen_rgb(x, y, w, h):
    result = (ctypes.c_ubyte * (w * h * 3))()
    screen.get_image_grey(x, y, w, h, result)
    return Image.frombuffer('RGB', (w, h), result, 'raw', 'RGB', 0, 1)

def grab_screen_grey(x, y, w, h):
    result = (ctypes.c_ubyte * (w * h))()
    screen.get_image_grey(x, y, w, h, result)
    return result

def get_image_grey(w, h, array):
    return Image.frombuffer('L', (w, h), array, 'raw', 'L', 0, 1)

if __name__ == '__main__':
    init()
    im = grab_screen(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    im.save(sys.argv[5], 'JPEG')
    destroy()
