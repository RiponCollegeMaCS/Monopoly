#!/usr/bin/env python3
###############################################################################
#
# Connects to the C standard library to do fast(er) random number
# generation.  Preliminary results show at least a 2x speedup with
# no loss of randomness.
#
# Author: Braxton Schafer <braxton.schafer@gmail.com> (bjs)
# Organization: Ripon College
#
# Date Created: 13/4/15
#
# Changelog:
#
###############################################################################

import ctypes
import sys

libc = None

if sys.platform == 'linux':
    libc = ctypes.cdll.LoadLibrary("libc.so.6")
elif sys.platform == 'darwin':
	libc = ctypes.cdll.LoadLibrary("libSystem.dylib")
elif sys.platform == 'win32':
	libc = ctypes.cdll.LoadLibrary("msvcrt.dll") # hopefully this'll work

def roll():
	libc.srand(libc.time(None) + libc.rand())
	return libc.rand() % 6 + 1
    # return next(_roll())

def choice(lst):
    # Initialize and seed
    libc.srand(libc.time(None))
    return lst[libc.rand() % len(lst)]


def shuffle(lst):
    # Initialize and seed
    libc.srand(libc.time(None))
    for i in range(len(lst)):
        j = libc.rand() % (len(lst) - i) + i
        lst[i], lst[j] = lst[j], lst[i]

if __name__ == '__main__':
	for i in range(100000):
		print(roll())