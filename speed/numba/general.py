# coding: utf-8

import numpy as np
from numba import double
import numba as nb
from numba import jit
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


# pairwise_numba = jit(pairwise_python)

# 用numba加速的求和函数
@nb.jit
def nb_sum(a):
    Sum = 0
    for i in range(len(a)):
        Sum += a[i]
    return Sum

# 没用numba加速的求和函数
def py_sum(a):
    Sum = 0
    for i in range(len(a)):
        Sum += a[i]
    return Sum


if __name__ == '__main__':
    import time
    import numpy as np

    l = np.linspace(0, 100, 100)  # 创建一个长度为100的数组

    start = time.time()
    # py_sum(l)
    nb_sum(l)
    end = time.time()
    print('elapse:', end -start)
