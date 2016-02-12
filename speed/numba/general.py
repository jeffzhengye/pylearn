# coding: utf-8

import numpy as np
from numba import double
import numba as nb
from numba.decorators import jit, autojit
# from IPython import get_ipython
# ipython = get_ipython()


def pairwise_python(X):
    M = X.shape[0]
    N = X.shape[1]
    D = np.empty((M, M), dtype=np.float)
    for i in range(M):
        for j in range(M):
            d = 0.0
            for k in range(N):
                tmp = X[i, k] - X[j, k]
                d += tmp * tmp
            D[i, j] = np.sqrt(d)
    return D


def pairwise_numpy(X):
    return np.sqrt(((X[:, None, :] - X) ** 2).sum(-1))


pairwise_numba = autojit(pairwise_python)