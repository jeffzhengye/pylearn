import theano
import numpy
import numpy as np
from theano import tensor as T

__author__ = 'Jeff Ye'


def print_ndarray_shape():
    """
    this shows how to print ndarray shape as well as the change before and after executing the function.
    link: http://deeplearning.net/software/theano/tutorial/debug_faq.html#how-do-i-print-an-intermediate-value-in-a-function-method
    """

    def inspect_inputs(i, node, fn):
        print i, node, "\ninput(s) value(s):", [input[0].shape for input in fn.inputs],

    def inspect_outputs(i, node, fn):
        print "\noutput(s) value(s):", [output[0] for output in fn.outputs]

    x = theano.tensor.matrix('x')
    f = theano.function([x], [5 * x],
                        mode=theano.compile.MonitorMode(
                            pre_func=inspect_inputs,
                            post_func=inspect_outputs))
    f(numpy.arange(10).reshape(2, 5))


def print_detect_nan():
    def detect_nan(i, node, fn):
        for output in fn.outputs:
            if not isinstance(output[0], numpy.random.RandomState) and numpy.isnan(output[0]).any():
                print '*** NaN detected ***'
                theano.printing.debugprint(node)
                print 'Inputs : %s' % [input[0] for input in fn.inputs]
                print 'Outputs: %s' % [output[0] for output in fn.outputs]
                break

    x = theano.tensor.dscalar('x')
    f = theano.function([x], [theano.tensor.log(x) * x],
                        mode=theano.compile.MonitorMode(
                            post_func=detect_nan))
    f(0)  # log(0) * 0 = -inf * 0 = NaN


def test_value():
    from keras.layers.core import Dense
    from theano import pp, function
    theano.config.compute_test_value = 'warn'

    # since the test input value is not aligned with the requirement in Dense,
    # it will report error quickly. Change 100 to 1000 will be fine.
    t_value = np.zeros((500, 1000), dtype=np.float32)
    X = T.matrix()
    X.tag.test_value = t_value
    d = Dense(200, input_dim=1000)
    # d1 = Dense(200, input_dim=1000)
    d.build()
    z = d(X)
    f = function([X], z)
    # turn it off after
    theano.config.compute_test_value = 'off'

if __name__ == "__main__":
    test_value()
