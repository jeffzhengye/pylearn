# -*- coding: utf-8 -*-
'''
  @author: jeffzhengye
  @contact: yezheng@scuec.edu.cn
  @file: tf_dataset_from_generator_args.py
  @time: 2021/1/5 16:27
  @desc:
 '''

import tensorflow as tf
import numpy as np
import collections


def movingWindow(data, window_size):
    print(type(window_size))
    window_size = int( window_size )
    buffer = collections.deque(data[:window_size - 1], maxlen=window_size)
    for i, datum in enumerate(data[window_size - 1:]):
        buffer.append(datum)
        for b in buffer:
            yield datum, b


window_size = 2
data = np.arange(10)

dataset = tf.data.Dataset.from_generator(
    movingWindow,
    args=(data, window_size),
    output_types=(np.int32, np.int32)
)

print(next(movingWindow(data, window_size)))
print(next(iter(dataset)))
