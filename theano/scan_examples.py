import theano
from theano import tensor as T
import numpy as np

__author__ = 'Jeff Ye'


def scan_matrix():
    def slide_sum(i, size, X):
        return T.sum(X[i:i+size], axis=0), theano.scan_module.until(i >= X.shape[0] - size)
    M = np.arange(20).reshape([5, 4])
    print(M)

    x = T.matrix('x')
    window_size = T.iscalar('w')
    sum_fun, _ = theano.scan(slide_sum, sequences=T.arange(x.shape[0]), non_sequences=[window_size, x])
    f = theano.function([window_size, x], sum_fun)

    print(f(2, M))


def scan_tensor3():
    def slide_sum(i, size, X):
        return T.sum(X[:, i:i+size, :], axis=1), theano.scan_module.until(i >= X.shape[0] - size)
    M = np.arange(64).reshape([4, 4, 4])
    print(M)

    x = T.tensor3('x')
    window_size = T.iscalar('w')
    sum_fun, _ = theano.scan(slide_sum, sequences=T.arange(x.shape[0]), non_sequences=[window_size, x])
    f = theano.function([window_size, x], sum_fun)

    print(f(2, M))


def power_of_2(previous_power, max_value):
    return previous_power*2, theano.scan_module.until(previous_power*2 > max_value)


def scan_util():
    max_value = T.scalar()
    values, _ = theano.scan(power_of_2,
                            outputs_info=T.constant(1.),
                            non_sequences=max_value,
                            n_steps=1024)

    f = theano.function([max_value], values)
    print f(45)


def scan_with_output():
    def _step(x, y, z):
        return x + y + z, y+z
    k = T.vector("k", dtype='float64')
    a = T.vector('a', dtype='float64')
    o = theano.shared(value=np.asarray(0, dtype='float64'), strict=False)
    results, _ = theano.scan(
        _step,
        sequences=[a, k],
        outputs_info=[None, o])

    f = theano.function([a, k], outputs=results)
    print(f(np.arange(10), np.arange(10)))

if __name__ == "__main__":
    # scan_matrix()
    # scan_tensor3()
    # scan_util()
    scan_with_output()
