__author__ = 'jeffye'

# https://github.com/tensorflow/fold/blob/master/tensorflow_fold/g3doc/quick.ipynb
# fold block
# https://github.com/tensorflow/fold/blob/master/tensorflow_fold/g3doc/blocks.md#using-tensorflow-tensors
# boilerplate
import random
import tensorflow_learning as tf

sess = tf.InteractiveSession()
import tensorflow_fold as td

scalar_block = td.Scalar()
vector3_block = td.Vector(3)



def block_info(block):
    print("%s: %s -> %s" % (block, block.input_type, block.output_type))


block_info(scalar_block)

print scalar_block.eval(42).shape
print(type(vector3_block.eval([1, 2, 3])))
print (td.Map(td.Scalar()) >> td.Reduce(td.Function(tf.multiply))).eval(range(1, 10))

mul_value = 1
for i in range(1, 10):
    mul_value *= i
print mul_value

print (td.Map(td.Scalar()) >> td.Fold(td.Function(tf.divide), tf.ones([]))).eval(range(1, 5))
print (td.Map(td.Scalar()) >> td.Reduce(td.Function(tf.divide), tf.ones([]))).eval(range(1, 5))
