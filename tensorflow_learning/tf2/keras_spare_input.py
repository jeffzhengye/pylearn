# encoding: utf-8
'''
  @author: jeffzhengye
  @contact: yezheng@scuec.edu.cn
  @file: structured_data.py
  @time: 2020/12/23 11:27
  @desc: 样例： 如何使用sparse input 高效处理数据
  '''

import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Input
from keras.models import Model
import scipy
import numpy as np
from scipy.sparse import coo_matrix


class DenseLayerForSparse(tf.keras.layers.Layer):
    def __init__(self, vocabulary_size, num_units, activation, **kwargs):
        super(DenseLayerForSparse, self).__init__()
        self.vocabulary_size = vocabulary_size
        self.num_units = num_units
        self.activation = tf.keras.activations.get(activation)

    def build(self, input_shape):
        self.kernel = self.add_variable(
            "kernel", shape=[self.vocabulary_size, self.num_units]
        )
        self.bias = self.add_variable("bias", shape=[self.num_units])

    def call(self, inputs, **kwargs):
        if isinstance(inputs, tf.SparseTensor):
            outputs = tf.add(tf.sparse.matmul(inputs, self.kernel), self.bias)
        if not isinstance(inputs, tf.SparseTensor):
            outputs = tf.add(tf.matmul(inputs, self.kernel), self.bias)
        return self.activation(outputs)

    def compute_output_shape(self, input_shape):
        input_shape = input_shape.get_shape().as_list()
        return input_shape[0], self.num_units


# It is possible to use sparse matrices as inputs to a Keras model
# if you write a custom training loop.
# In the example below, the model takes a sparse matrix as an input and outputs a dense matrix.

trainX = scipy.sparse.random(1024, 1024)
weights = trainX
# print(trainX[:2])
# trainX.sort_indices()

order = np.lexsort((weights.col, weights.row))
sorted_weights = coo_matrix((weights.data[order], (weights.row[order], weights.col[order])),
                            shape=weights.shape)
trainX = sorted_weights
trainY = np.random.rand(1024, 1024)
# tf.sparse.SparseTensor

inputs = Input(shape=(trainX.shape[1],), sparse=True)
# inputs = Input(sparse=True)
outputs = Dense(trainY.shape[1], activation='softmax')(inputs)
model = Model(inputs=inputs, outputs=outputs)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x=trainX, y=trainY)

steps = 10
# for i in range(steps):
#     # For simplicity, we directly use trainX and trainY in this example
#     # Usually, this is where batches are prepared
#     print(model.train_on_batch(trainX, trainY))
# [3549.2546, 0.0]
# ...
# [3545.6448, 0.0009765625]
