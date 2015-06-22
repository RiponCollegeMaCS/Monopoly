from timer import timer

'''
import random

import numpy

def method1(num):
    numbers = [random.randint(1, 6) for i in range(num)]

def method2(num):
    numbers = numpy.random.randint(6, size=num)
    print(numbers[0:10])

a = [1,2]
print(a.pop())
print(a)
print(a.pop())
print(a)
try:
    print(a.pop())
    print(a)
except:
    print("*")

timer()
method1(1000000)
timer()

rolls = numpy.random.randint(6, size=5000)
roll_index = -1

def get_roll():
    roll_index = 0
    roll_index += 1
    return rolls[roll_index] + 1

print(get_roll())
timer()
method2(1000000)
timer()

'''

import timeit
from ctypes import cdll


def generate_c(num):
    nums = []
    libc = cdll.msvcrt  # Windows
    while num:
        yield (libc.rand() % 6) + 1
        num -= 1


nums = []

timer()
nums = [i for i in generate_c(100000)]
timer()

import random

nums = []

timer()
nums = [random.randint(1,6) for i in range(100000)]
timer()

import numpy

timer()
rolls = numpy.random.randint(6, size=100000)
timer()