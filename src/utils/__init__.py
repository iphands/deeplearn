import json
import re
import Xlib
import Xlib.display

def get_geometry(window):
    data = window.get_geometry()._data
    return {
        'x': data['x'],
        'y': data['y'],
        'w': data['width'],
        'h': data['height']
    }

def print_geo(window):
    print(json.dumps(get_geometry(window)))

def print_sizes(r, depth):
    spaces = "  " * depth
    for window in r.query_tree().children:
        name = window.get_wm_name()
        if name and re.match('.*snes.*', name, re.IGNORECASE):
            print("{}({}){}".format(spaces, len(window.query_tree().children), window.get_wm_name()))
            print_geo(spaces, window.get_geometry()._data)
            print_parents(spaces, window)
        print_sizes(window, depth + 1)

def print_parents(spaces, w):
    parent = w.query_tree().parent
    if parent:
        print(w.get_wm_class())
        print_geo(spaces, parent.get_geometry()._data)
        print_parents(spaces, parent)


def find_window(nameRegex, root=None):
    if not root: root = Xlib.display.Display().screen().root

    for window in root.query_tree().children:
        name = window.get_wm_name()
        if name and re.match(nameRegex, name):
            return window
        result = find_window(nameRegex, root=window)
        if result:
            return result

def get_hier(window):
    root = Xlib.display.Display().screen().root
    lst = [ window ]

    def loop(w, l):
        if w == 0 or w == root: return
        parent = w.query_tree().parent
        if parent == 0: return
        l.append(parent)
        loop(parent, l)

    loop(window, lst)
    return lst
