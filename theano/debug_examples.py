import theano
import numpy

__author__ = 'Jeff Ye'


def print_ndarray_shape():
    """
    this shows how to print ndarray shape as well as the change before and after executing the function.
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


if __name__ == "__main__":
    print_ndarray_shape()