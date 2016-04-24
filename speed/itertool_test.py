# encoding: utf-8
import itertools
from numba import jit
import numpy as np

x = range(10000)
y = range(10000)


def zip_base(x, y):
    """
    1000 loops, best of 3: 734 µs per loop
    """
    s = 0
    for i, j in zip(x, y):
        s += i * j
    return s


def izip_base(x, y):
    """
    1000 loops, best of 3: 525 µs per loop
    """
    s = 0
    for i, j in itertools.izip(x, y):
        s += i * j
    return s


def np_zip_base(x, y):
    """
    1000 loops, best of 3: 1.4 ms per loop
    """
    x = np.array(x)
    y = np.array(y)
    return np.sum(x * y)

# 1000 loops, best of 3: 678 µs per loop
nb_zip_base = jit(zip_base)

# 1000 loops, best of 3: 1.08 ms per loop
nb_izip_base = jit(izip_base)

# raise error.
nb_np_zip_base = jit(np_zip_base)