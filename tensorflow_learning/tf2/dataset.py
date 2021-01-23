# -*- coding: utf-8 -*-
'''
  @author: jeffzhengye
  @contact: yezheng@scuec.edu.cn
  @file: dataset.py
  @time: 2021/1/7 14:20
  @desc:
 '''

import tensorflow as tf

def test_cache_dataset():
    def map_fun(x):
        print(x, type(x))
        return 2 * x
    d = tf.data.Dataset.range(5)
    d = d.map(map_fun).cache("test.tfdataset")
    for i in d:
        # print(i)
        pass


if __name__=='__main__':
    test_cache_dataset()