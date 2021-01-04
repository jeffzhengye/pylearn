import numpy as np
import tensorflow as tf

# from: https://www.tensorflow.org/lite/convert/python_api?hl=zh-cn
print('version:', tf.__version__)


def from_saved_model():
    """
    以下示例展示了如何将一个 SavedModel 转换为 TensorFlow Lite 中的 FlatBuffer格式。
    :return:
    """
    # 建立一个简单的模型。
    root = tf.train.Checkpoint()
    root.v1 = tf.Variable(3.)
    root.v2 = tf.Variable(2.)
    root.f = tf.function(lambda x: root.v1 * root.v2 * x)

    # 保存模型。
    export_dir = "/tmp/test_saved_model"
    input_data = tf.constant(1., shape=[1, 1])
    to_save = root.f.get_concrete_function(input_data)
    tf.saved_model.save(root, export_dir, to_save)

    # 转换模型。
    converter = tf.lite.TFLiteConverter.from_saved_model(export_dir)
    tflite_model = converter.convert()
    # Save the model.
    with open('model.tflite', 'wb') as f:
      f.write(tflite_model)

def from_saved_model_support_specifying_input_dimension():
    """
    以上 API 不支持指定输入向量的维度。 如果您的模型需要指定输入向量的维度，请使用 from_concrete_functions 来完成。 示例：
    :return:
    """
    root = tf.train.Checkpoint()
    root.v1 = tf.Variable(3.)
    root.v2 = tf.Variable(2.)
    root.f = tf.function(lambda x: root.v1 * root.v2 * x)

    # 保存模型。
    export_dir = "/tmp/test_saved_model"
    input_data = tf.constant(1., shape=[1, 1])
    to_save = root.f.get_concrete_function(input_data)
    tf.saved_model.save(root, export_dir, to_save)

    # 转换模型。
    model = tf.saved_model.load(export_dir)
    concrete_func = model.signatures[
        tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
    concrete_func.inputs[0].set_shape([1, 256, 256, 3])
    converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])


def from_keras_model():
    # 创建一个简单的 Keras 模型。
    x = [-1, 0, 1, 2, 3, 4]
    y = [-3, -1, 1, 3, 5, 7]

    model = tf.keras.models.Sequential(
        [tf.keras.layers.Dense(units=1, input_shape=[1])])
    model.compile(optimizer='sgd', loss='mean_squared_error')
    model.fit(x, y, epochs=50)

    # 转换模型。
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()


def end_2_end_MobileNet():
    """
    端到端 MobileNet 转换
以下示例展示了如何将将一个提前训练好的 tf.keras MobileNet 模型转换为 TensorFlow Lite 支持的类型并运行推断 （inference）。
随机数据分别在 TensorFlow 和 TensorFlow Lite 模型中运行的结果将被比较。如果是从文件加载模型，请使用 model_path 来代替 model_content。
    :return:
    """
    # 加载 MobileNet tf.keras 模型。
    model = tf.keras.applications.MobileNetV2(
        weights="imagenet", input_shape=(224, 224, 3))

    # 转换模型。
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    # 加载 TFLite 模型并分配张量（tensor）。
    interpreter = tf.lite.Interpreter(model_content=tflite_model)
    interpreter.allocate_tensors()

    # 获取输入和输出张量。
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print('input_details', input_details)
    print('output_details', output_details)

    # 使用随机数据作为输入测试 TensorFlow Lite 模型。
    input_shape = input_details[0]['shape']
    input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    # 函数 `get_tensor()` 会返回一份张量的拷贝。
    # 使用 `tensor()` 获取指向张量的指针。
    tflite_results = interpreter.get_tensor(output_details[0]['index'])

    # 使用随机数据作为输入测试 TensorFlow 模型。
    tf_results = model(tf.constant(input_data))

    # 对比结果。
    for tf_result, tflite_result in zip(tf_results, tflite_results):
      np.testing.assert_almost_equal(tf_result, tflite_result, decimal=5)