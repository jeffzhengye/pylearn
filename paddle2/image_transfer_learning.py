# -*- coding: utf-8 -*-
'''
  @author: jeffzhengye
  @contact: yezheng@scuec.edu.cn
  @file: image_transfer_learning.py.py
  @time: 2020/12/26 21:03
  @desc: 飞桨2x, 如何使用迁移学习简单样例。
 '''

import paddle
from paddle.vision.transforms import Compose, Resize, ColorJitter, RandomHorizontalFlip, RandomRotation, Resize
from paddle.io import Dataset

model = paddle.vision.models.resnet18()
model.parameters()
paddle.vision.models.vgg19()
# model.train() #训练模式
cross_entropy = paddle.nn.CrossEntropyLoss()
opt=paddle.optimizer.SGD(learning_rate=0.001, parameters=model.parameters())

epochs_num= 30
model = paddle.Model(model)
# 为模型训练做准备，设置优化器，损失函数和精度计算方式
model.prepare(optimizer=paddle.optimizer.Adam(parameters=model.parameters()),
              loss=paddle.nn.CrossEntropyLoss(),
              metrics=paddle.metric.Accuracy())
model.summary()

paddle.callbacks
paddle.vision.models.resnet50().parameters()
metrics=paddle.metric.Accuracy()
paddle.concat()

class MyAccuracy(paddle.metric.Accuracy):
    def compute(self, pred, label, *args):
        label = label[:, :1]
        return super(MyAccuracy, self).compute(pred, label, *args)

paddle.summary(

)

from paddle.vision.transforms import Compose, Resize, ColorJitter


# 定义想要使用那些数据增强方式，这里用到了随机调整亮度、对比度和饱和度，改变图片大小
transform = Compose([ColorJitter(), Resize(size=100)])

from paddle.vision.transforms import Compose, Resize, ColorJitter


model.load()

model.fit(train_dataset,
          epochs=40,
          batch_size=32,
          verbose=1)


model.save('reset18')
