---
tasks:
- multi-modal-embedding
- image-text-retrieval
domain:
- multi-modal
frameworks:
- pytorch
backbone:
- vit-base-patch16, RoBERTa-wwm-ext-base-chinese
metrics:
- R@1
license: Apache License 2.0
tags:
- Alibaba
- multi-modal-embedding
datasets:
  evaluation:
  - modelscope/muge
  train:
  - modelscope/muge
finetune-support: True
widgets:
  - inputs:
      - validator:
          max_words: 75
        type: text
        title: 查询文本
    output:
      maximize: false
    examples:
      - name: 1
        inputs:
          - data: 戴眼镜的猫
      - name: 2
        inputs:
          - data: 一个在逛公园的女孩
    task: multi-modal-embedding
---

<p align="center">
    <br>
    <img src="resources/Chinese_CLIP_logo_tp_path.svg" width="400" />
    <br>
<p>
<br>

# 中文CLIP
## News
- 2022年11月：
  - 发布ModelScope 1.0版本，以下能力请使用1.0.2及以上版本。
  - 上线[Huge模型(224分辨率)](https://www.modelscope.cn/#/models/damo/multi-modal_clip-vit-huge-patch14_zh/summary)
  - 上线创空间，更强大的demo展示：[中文图文检索应用](https://modelscope.cn/studios/damo/chinese_clip_applications/summary)
  - 支持finetune能力，具体参考[中文CLIP Tutorial](https://modelscope.cn/docs/%E4%B8%AD%E6%96%87CLIP%20Tutorial) 3.3节。
  - 推出[中文CLIP论文](https://arxiv.org/abs/2211.01335)，欢迎查阅更多细节。

- 2022年09月: 现在已经上线[Large336分辨率模型](https://www.modelscope.cn/#/models/damo/multi-modal_clip-vit-large-patch14_336_zh/summary)，我们训练时image侧分辨率为336*336像素，效果更好，欢迎试用。

## 模型与项目介绍

本项目为[CLIP](https://arxiv.org/abs/2103.00020)模型的中文版本，使用大规模中文数据进行训练（**~2亿图文对**），可用于图文检索和图像、文本的表征提取，应用于搜索、推荐等应用场景。

CLIP模型是来自OpenAI的经典图文表征模型，其采用双塔模型结构（如下图），利用大规模图文对平行语料进行对比学习，从而能够实现图片和文本的跨模态语义特征抽取。

<p align="center">
<img src="resources/clip_model.png" alt="CLIP模型结构"  width="400" />

原始的CLIP模型基于英文图文语料，不能用于中文的图文表征提取场景。本项目以英文CLIP视觉侧参数和中文Roberta参数，作为模型初始化值。
基于大规模原生中文图文数据，通过如下图所示的二阶段预训练策略（一阶段仅训练文本侧，二阶段同时训练），实现了CLIP模型的中文化版本，未来将在此持续更新。

<p align="center">
<img src="resources/chinese_clip_pretrain.png" alt="中文CLIP预训练机制"  width="400" />
<br><br>

本系列还有如下模型，欢迎试用：
- [Large224分辨率模型](https://www.modelscope.cn/#/models/damo/multi-modal_clip-vit-large-patch14_zh/summary)
- [Large336分辨率模型](https://www.modelscope.cn/#/models/damo/multi-modal_clip-vit-large-patch14_336_zh/summary)
- [Huge224分辨率模型](https://www.modelscope.cn/#/models/damo/multi-modal_clip-vit-huge-patch14_zh/summary)

## 快速用起来
提取特征不过区区数行代码，就可以通过我们的服务得到图像或文本的特征。如果你觉得还不够方便，请点击右上角`Notebook`按钮，我们为你提供了配备了GPU的环境，你只需要在notebook里输入提供的代码，就可以把中文CLIP玩起来了！

注：使用`Notebook`要验证下当前modelscope的版本号，如果版本低于0.3.7，可以点击更新镜像并启动，如下图所示：

<img src="resources/maas_update_image.png" alt="如何更新镜像"  width="450" />

**让我们开始代码实例**
<p align="center">
    <img src="resources/pokemon.jpeg" alt="皮卡丘" width="200" />

```python
# require modelscope>=0.3.7
# 按照更新镜像的方法处理或者下面的方法
# pip install --upgrade modelscope -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html
import torch
from modelscope.utils.constant import Tasks
from modelscope.pipelines import pipeline
from modelscope.preprocessors.image import load_image

pipeline = pipeline(task=Tasks.multi_modal_embedding,
    model='damo/multi-modal_clip-vit-base-patch16_zh')
input_img = load_image('https://yangan2.oss-cn-beijing.aliyuncs.com/pokemon.jpeg') # 支持皮卡丘示例图片路径/本地图片 返回PIL.Image
input_texts = ["杰尼龟", "妙蛙种子", "小火龙", "皮卡丘"]

# 支持一张图片(PIL.Image)或多张图片(List[PIL.Image])输入，输出归一化特征向量
img_embedding = pipeline.forward({'img': input_img})['img_embedding'] # 2D Tensor, [图片数, 特征维度]

# 支持一条文本(str)或多条文本(List[str])输入，输出归一化特征向量
text_embedding = pipeline.forward({'text': input_texts})['text_embedding'] # 2D Tensor, [文本数, 特征维度]

# 计算图文相似度
with torch.no_grad():
    # 计算内积得到logit，考虑模型temperature
    logits_per_image = (img_embedding / pipeline.model.temperature) @ text_embedding.t()
    # 根据logit计算概率分布
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

print("图文匹配概率:", probs)
```
<br>

## 为什么中文CLIP是你的最佳选择？
我们实现的中文版本CLIP在多个公开数据集上取得杰出的效果，基本超出市面同类型baseline模型。具体评测数据集包括MUGE（欢迎访问[官网](https://tianchi.aliyun.com/muge)），Flickr30K-CN和COCO-CN， 结果如下所示：

### MUGE Text-to-Image Retrieval
<table border="1" width="100%">
    <tr align="center">
        <th>Setup</th><th colspan="4">Zero-shot</th><th colspan="4">Finetune</th>
    </tr>
    <tr align="center">
        <td>Metric</td><td>R@1</td><td>R@5</td><td>R@10</td><td>MR</td><td>R@1</td><td>R@5</td><td>R@10</td><td>MR</td>
    </tr>
    <tr align="center">
        <td>Wukong<sub>ViT-B</sub></td><td>33.4</td><td>59.3</td><td>69.7</td><td>54.1</td><td>39.2</td><td>66.9</td><td>77.4</td><td>61.2</td>
	</tr>
	<tr align="center">
        <td>R2D2<sub>ViT-B</sub></td><td>-</td><td>-</td><td>-</td><td>-</td><td>47.4</td><td>75.1</td><td>83.5</td><td>68.7</td>
	</tr>
	<tr align="center">
        <td>CN-CLIP<sub>ViT-B</sub></td><td><b>52.1</b></td><td><b>76.7</b></td><td><b>84.4</b></td><td><b>71.1</b></td><td><b>58.4</b></td><td><b>83.6</b></td><td><b>90.0</b></td><td><b>77.4</b></td>
	</tr>
</table>


### Flickr30K-CN Retrieval
<table border="1" width="100%">
	<tr align="center">
        <th>Task</th><th colspan="6">Text-to-Image</th><th colspan="6">Image-to-Text</th>
    </tr>
    <tr align="center">
        <th>Setup</th><th colspan="3">Zero-shot</th><th colspan="3">Finetune</th><th colspan="3">Zero-shot</th><th colspan="3">Finetune</th>
    </tr>
    <tr align="center">
        <td>Metric</td><td>R@1</td><td>R@5</td><td>R@10</td><td>R@1</td><td>R@5</td><td>R@10</td><td>R@1</td><td>R@5</td><td>R@10</td><td>R@1</td><td>R@5</td><td>R@10</td>
    </tr>
    <tr align="center">
        <td>Wukong<sub>ViT-B</sub></td><td>45.7</td><td>73.8</td><td>82.2</td><td>67.6</td><td>89.6</td><td>94.2</td><td>66.2</td><td>88.7</td><td>94.3</td><td>83.9</td><td>97.6</td><td>99.0</td>
	</tr>
	<tr align="center">
        <td>R2D2<sub>ViT-B</sub></td><td>-</td><td>-</td><td>-</td><td>78.3</td><td>94.6</td><td>97.0</td><td>-</td><td>-</td><td>-</td><td>92.6</td><td><b>99.1</b></td><td><b>99.8</b></td>
	</tr>
	<tr align="center">
        <td>CN-CLIP<sub>ViT-B</sub></td><td><b>62.7</b></td><td><b>86.9</b></td><td><b>92.8</b></td><td><b>79.1</b></td><td><b>94.8</b></td><td><b>97.4</b></td><td><b>74.6</b></td><td><b>93.5</b></td><td><b>97.1</b></td><td><b>93.5</b></td><td>99.0</td><td>99.5</td>
	</tr>
</table>


### COCO-CN Retrieval
<table border="1" width="100%">
	<tr align="center">
        <th>Task</th><th colspan="6">Text-to-Image</th><th colspan="6">Image-to-Text</th>
    </tr>
    <tr align="center">
        <th>Setup</th><th colspan="3">Zero-shot</th><th colspan="3">Finetune</th><th colspan="3">Zero-shot</th><th colspan="3">Finetune</th>
    </tr>
    <tr align="center">
        <td>Metric</td><td>R@1</td><td>R@5</td><td>R@10</td><td>R@1</td><td>R@5</td><td>R@10</td><td>R@1</td><td>R@5</td><td>R@10</td><td>R@1</td><td>R@5</td><td>R@10</td>
    </tr>
    <tr align="center">
        <td>Wukong<sub>ViT-B</sub></td><td>49.2</td><td>79.4</td><td>87.9</td><td>67.0</td><td>91.4</td><td>96.7</td><td>48.3</td><td>77.8</td><td>88.8</td><td>65.8</td><td>90.3</td><td>96.6</td>
	</tr>
	<tr align="center">
        <td>R2D2<sub>ViT-B</sub></td><td>-</td><td>-</td><td>-</td><td>75.1</td><td>94.2</td><td>98.1</td><td>-</td><td>-</td><td>-</td><td>76.1</td><td>95.3</td><td>98.5</td>
	</tr>
	<tr align="center">
        <td>CN-CLIP<sub>ViT-B</sub></td><td><b>62.2</b></td><td><b>86.6</b></td><td><b>94.9</b></td><td><b>77.0</b></td><td><b>97.1</b></td><td><b>99.0</b></td><td><b>57.0</b></td><td><b>84.1</b></td><td><b>93.6</b></td><td><b>77.4</b></td><td><b>96.2</b></td><td><b>98.9</b></td>
	</tr>
</table>
<br><br>

## 模型训练流程

### 训练数据介绍
本模型训练数据集是预训练数据集。

### 训练流程
finetune具体方法请您查阅[中文CLIP Tutorial](https://modelscope.cn/docs/%E4%B8%AD%E6%96%87CLIP%20Tutorial) 3.3节。

## 使用方式及场景
使用方式：
- 对输入的图像、文本数据进行特征提取

使用场景:
- 通用的图文跨模态检索任务
- 通用图文特征提取器
<br><br>


## 模型局限性以及可能的偏差
训练数据集自身有局限，有可能产生一些偏差，请用户自行评测后决定如何使用。

## 相关引用
关于中文clip，我们已经推出了相关论文，有更多细节可以查阅，如对您的工作有帮助，欢迎引用。
```
@article{chinese-clip,
  title={Chinese CLIP: Contrastive Vision-Language Pretraining in Chinese},
  author={Yang, An and Pan, Junshu and Lin, Junyang and Men, Rui and Zhang, Yichang and Zhou, Jingren and Zhou, Chang},
  journal={arXiv preprint arXiv:2211.01335},
  year={2022}
}
```
