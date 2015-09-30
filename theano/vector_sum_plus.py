import theano
from theano import tensor as T

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
