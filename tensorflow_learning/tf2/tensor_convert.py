# -*- coding: utf-8 -*-
'''
  @author: jeffzhengye
  @contact: yezheng@scuec.edu.cn
  @file: tensor_convert.py
  @time: 2021/1/20 11:20
  @desc:
 '''

import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.framework import smart_cond
from tensorflow.python.keras import backend as K
from tensorflow.python.ops import math_ops
import numpy as np


# def add(preds, labels):
#     raw_arr = np.column_stack((preds, labels))
#     raw_arr = sorted(raw_arr, key=lambda d: d[0])
#
#     auc = 0.
#     fp1, tp1, fp2, tp2 = 0., 0., 0., 0.
#     for record in raw_arr:
#         fp2 += 1 - record[1]
#         tp2 += record[1]
#         auc += (fp2 - fp1) * (tp2 + tp1)
#         fp1, tp1 = fp2, tp2
#
#     threshold = len(preds) - 1e-3
#     # print('auc', auc, res = (1.0 - auc / (2.0 * tp2 * fp2)))
#     if tp2 > threshold or fp2 > threshold:
#         print('%s invalid batch' % "auc")
#         # return
#
#     if tp2 * fp2 > 0.0:
#         res = (1.0 - auc / (2.0 * tp2 * fp2))
#         return res
#     else:
#         return None
#
# res = add([0, 0, 0, 1], [0, 0, 0, 0])
# print('res', res)

m = tf.metrics.AUC(num_thresholds=5)
# m.update_state([0, 0, 0, 0], [0, 0, 0, 1])
# m.update_state([0, 0, 0, 1], [0, 0, 0, 1])
# print(m.result())
# m.reset_states()
# m.update_state([0, 0, 0, 1], [0, 0, 0, 0])
# m.update_state([0, 0, 0, 1], [0, 0, 0, 1])
# print(m.result())
#
# m.reset_states()
# m.update_state([0, 0, 0, 0], [0, 0, 0, 1])
# # m.update_state([0, 0, 0, 1], [0, 0, 0, 1])
# print(m.result())
#
# m.reset_states()
# # m.update_state([0, 0, 0, 0], [0, 0, 0, 1])
# m.update_state([0, 0, 0, 1], [0, 0, 0, 1])
# print(m.result())

# m.reset_states()
# # m.update_state([0, 0, 0, 0], [0, 0, 0, 1])
# m.update_state([0, 0, 0, 0], [0, 0, 0, 0])
# print(m.thresholds)
# print(m.true_positives)
# print(m.true_negatives)
# print(m.false_positives)
# print(m.false_negatives)
# print('auc:', m.result())
#
# recall = math_ops.div_no_nan(m.true_positives, m.true_positives + m.false_negatives)
# fp_rate = math_ops.div_no_nan(m.false_positives, m.false_positives + m.true_negatives)
# x = fp_rate
# y = recall
# print()
# print(fp_rate)
# print(y)
# print()
#
#     # Note: the case ('PR', 'interpolation') has been handled above.
# heights = (y[:m.num_thresholds - 1] + y[1:]) / 2.
# print(x[:m.num_thresholds - 1] - x[1:])
# print(heights)

key=[1, 2, 3]
output_types = [tf.int32] * 3
output_shapes = dict([(k, tf.TensorShape((None, ))) for k in key])

def arr2sparse(arr):
    # arr_tensor = tf.constant(np.array(arr))
    arr_tensor = arr
    arr_idx = tf.where(tf.not_equal(arr_tensor, 0))
    # print(arr_tensor)
    # print(tf.shape(arr_tensor))
    indices = tf.cast(arr_idx, tf.int64)
    shape = tf.cast(tf.shape(arr_tensor), tf.int64)
    arr_sparse = tf.SparseTensor(arr_idx, tf.gather_nd(arr_tensor, arr_idx), shape)
    return arr_sparse

def generator():
    for i in range(1, 100):
        len_list = np.random.random_integers(1, 10, (3, ))
        values = [np.random.random_integers(0, high=10000000000, size=(j,)) for j in len_list]
        # print(indices, values, shape)
        # yield indices, values, shape
        yield dict(zip(key, values))

# dataset = tf.data.Dataset.from_generator(generator, (tf.int64, tf.float32, tf.int64))
dataset = tf.data.Dataset.from_generator(generator, dict(zip(key, output_types)),
                                         output_shapes=output_shapes)


def _to_sparse(d):
    y_dict = {}
    for k, v in d.items():
        y_dict[k] = arr2sparse(v)
    return y_dict

dataset = dataset.map(_to_sparse, num_parallel_calls=tf.data.experimental.AUTOTUNE)

# dataset = dataset.map(lambda i, v, s: tf.SparseTensor(i, v, s))

for i, one in dataset.batch(2).take(2).enumerate(0):
    # ss = tf.sparse_reduce_sum(one)
    # print(i, one)
    print('one', i.numpy(), one)
    print(one[1])
    # print('dense', tf.sparse.to_dense(one))

