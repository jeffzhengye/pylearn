# encoding: utf-8
'''
  @author: jeffzhengye
  @contact: yezheng@scuec.edu.cn
  @file: structured_data.py
  @time: 2020/12/23 11:27
  origin: https://www.tensorflow.org/tutorials/structured_data/feature_columns?hl=zh-cn
  @desc: 样例： 如何使用tf.feature_column 来处理结构化数据，
  '''

import numpy as np
import pandas as pd

import tensorflow as tf

from tensorflow import feature_column
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from tensorflow.python.framework import dtypes

tf.feature_column.numeric_column
keras.layers.DenseFeatures
tf.feature_column.embedding_column
tf.feature_column.categorical_column_with_hash_bucket
tf.feature_column.indicator_column
tf.feature_column.bucketized_column


# URL = 'https://storage.googleapis.com/applied-dl/heart.csv'
# dataframe = pd.read_csv(URL)
data_file = 'heart.csv'
dataframe = pd.read_csv(data_file)
dataframe = dataframe.replace({'thal': {0: 'normal', 1: "fixed", 2: "normal"}})
dataframe = dataframe.astype({'thal': str})
print(dataframe.head())

train, test = train_test_split(dataframe, test_size=0.2)
train, val = train_test_split(train, test_size=0.2)
print(len(train), 'train examples')
print(len(val), 'validation examples')
print(len(test), 'test examples')
print(train.head())

# 一种从 Pandas Dataframe 创建 tf.data 数据集的实用程序方法（utility method）
def df_to_dataset(dataframe, shuffle=True, batch_size=2):
    dataframe = dataframe.copy()
    labels = dataframe.pop('target')
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    return ds


batch_size = 3  # 小批量大小用于演示
train_ds = df_to_dataset(train, shuffle=False, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

for feature_batch, label_batch in train_ds.take(1):
    print('Every feature:', list(feature_batch.keys()))
    print('A batch of ages:', feature_batch['age'])
    print('A batch of targets:', label_batch)

# 我们将使用该批数据演示几种特征列
example_batch = next(iter(train_ds))[0]
print('example_batch', example_batch)
# sparse_input = {'indices':[[0, 0], [0, 1], [1, 2]], 'values': ['fixed', 'reversible',  'normal'], 'dense_shape': [2, 4]}
sparse_input = {'indices':[[0, 0], [0, 1], [1, 2]], 'values': [1, 1,  1], 'dense_shape': [2, 4]}
input_sparse = tf.sparse.SparseTensor(**sparse_input)
# input_sparse = tf.sparse.SparseTensor(indices=[[0, 0], [0, 1], [1, 2]], values=['fixed', 'reversible',  'normal'], dense_shape=[2, 4])
# example_batch = {
#     'thal': input_sparse
# }


# 用于创建一个特征列
# 并转换一批次数据的一个实用程序方法
def demo(feature_column):
    feature_layer = layers.DenseFeatures(feature_column)
    name = feature_column.name.split('_')[0]
    print('input:', example_batch[name])
    print(feature_layer(example_batch).numpy())


age = feature_column.numeric_column("age")
demo(age)
#
age_buckets = feature_column.bucketized_column(age, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])
demo(age_buckets)
#
# thal = feature_column.categorical_column_with_vocabulary_list(
#     'thal', ['fixed', 'normal', 'reversible'])

thal = feature_column.categorical_column_with_hash_bucket('thal', 20, dtype=dtypes.int32)
#
# thal_one_hot = feature_column.indicator_column(thal)
# demo(thal_one_hot)
# demo(thal)

# 注意到嵌入列的输入是我们之前创建的类别列
thal_embedding = feature_column.embedding_column(thal, dimension=8, combiner='sum')
# demo(thal_embedding)
