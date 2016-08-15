# encoding=utf8

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


"""
__author__ = 'jeffye'
uci medical data predication with pandas and sklearn
"""


input_file = u"胸外科手术1年后存活情况预测建模数据.txt"

# comma delimited is the default
df = pd.read_csv(input_file, header=0)
nd_data = df.as_matrix()
X = nd_data[:, 1:]
Y = nd_data[:, 0]
split_pos = int(X.shape[0] * 0.8)
print split_pos
# print X
# print Y
clf = RandomForestClassifier(n_estimators=100)
clf = clf.fit(X[:split_pos], Y[:split_pos])
print clf.score(X[:split_pos], Y[:split_pos])
print clf.score(X[split_pos:], Y[split_pos:]    )
