# coding: utf-8

import tensorflow as tf

print(tf.__version__)

saved_model_dir = "/mnt/d/code/faster_rcnn_inception_resnet_v2_640x640_1"

# converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
# tflite_model = converter.convert()
# open("converted_model.tflite", "wb").write(tflite_model)

graph_def_file = saved_model_dir + "/saved_model.pb"
input_arrays = ["input_1"]
output_arrays = ["lambda_5/add"]

converter = tf.lite.TFLiteConverter.from_frozen_graph(
    graph_def_file, input_arrays, output_arrays, input_shapes={"input_1": [1, 600, 600, 3]})
tflite_model = converter.convert()
open("wdsr_-x4-converted_model.tflite", "wb").write(tflite_model)
