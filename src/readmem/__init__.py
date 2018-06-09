#!/usr/bin/env python3
import ctypes
import os
import sys

readmem = ctypes.CDLL(os.path.dirname(os.path.realpath(__file__)) + '/readmem.so')
readmem.find_player_rank_address.restype = ctypes.c_long
address = None

def get_player_rank(pid, heap_start_address):
    global address
    if not address:
        address = readmem.find_player_rank_address(pid, ctypes.c_long(heap_start_address))
    return readmem.get_player_rank(24080, ctypes.c_long(address))

if __name__ == '__main__':
    print(get_player_rank())

