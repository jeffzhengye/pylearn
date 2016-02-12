import theano
from theano import tensor as T
import numpy as np

x = T.fmatrix('x')
v = T.fmatrix('v')
# y = v + T.sum(x, axis = 0)
# y = T.dot(x, v)
y = T.transpose(x) + v


# theano has better performance for matrix multiplication,
# but not as good for addition compared to numpy since numpy use multicores to do addition.
update_weight_theano = theano.function(inputs=[x, v],
                                       outputs=[y])


def update_weight_np(x, v):
    # return np.sum(x, axis=0) + v
    # return np.dot(x, v)
    return np.transpose(x) + v


def linear_combine():
    x = T.fmatrix('x')
    w = T.vector('w', 'float32')
    # z = T.dot(w, x)
    z = x * w
    f = theano.function(inputs=[x, w], outputs=z)
    print f(np.arange(4).reshape([2, 2]).astype('float32'), np.array([0.1, 0.2], dtype='float32'))


def linear_combine_shared():
    x = T.fmatrix('x')
    value = np.asarray(np.array([0.1, 0.2], dtype='float32'))
    w = theano.shared(value=value, strict=False)
    # w = T.vector('w', 'float32')
    z = T.dot(w, x)
    # z = x * w
    f = theano.function(inputs=[x], outputs=z)
    print f(np.arange(4).reshape([2, 2]).astype('float32'))


def weighting():
    from theano.tensor import TensorType

    x = T.ftensor3()
    # w = TensorType('float32', (False, False, True))()
    w = T.ftensor3()
    # z = T.dot(w, x)
    # y = T.addbroadcast(w, 2)
    # y = w.reshape([w.shape[0], w.shape[1]])
    y = T.flatten(w, 2)
    z = x * y


    f = theano.function(inputs=[x, w], outputs=z)
    input1 = np.arange(8).reshape([2, 2, 2]).astype('float32')
    input2 = np.array(
        [
            [
                [0.1], [0.2]
            ],
            [
                [0.2], [0.4]
            ]
        ]
    ).astype('float32')
    print input1, input1.shape
    print
    print input2, input2.shape
    print
    print f(input1, input2)
    # print input1 * input2


def weighting1():
    from theano.tensor import TensorType
    input1 = np.arange(12).reshape([3, 2, 2]).astype('float32')
    input2 = np.array(
        [1., 2., 3.]
    ).astype('float32')

    x = T.ftensor3()
    # w = TensorType('float32', (False, False, True))()
    w = theano.shared(value=input2, name='w', strict=False)
    y = (w * x.T).T

    f = theano.function(inputs=[x], outputs=y)
    print input1, input1.shape
    print
    print input2, input2.shape
    print
    print f(input1)
    # print input1 * input2


def concatenate():
    input = np.arange(12).reshape([2, 3, 2]).astype('float32')
    print input
    print
    pad_len = 1
    Y = T.tensor3()
    z = T.concatenate([Y[:, :pad_len, :], Y, Y[:, Y.shape[1] - pad_len:, :]], axis=1)
    f = theano.function(inputs=[Y], outputs=z)
    print f(input)

if __name__ == '__main__':
    # linear_combine()
    # linear_combine_shared()
    # weighting1()
    concatenate()