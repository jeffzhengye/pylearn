# -*- coding: utf-8 -*-
import os

import json
import shutil

from modelscope.metainfo import Metrics, Trainers
# 指标和训练器的Python类
from modelscope.msdatasets import MsDataset
# ModelScope集成数据集的Python类
from modelscope.trainers import build_trainer
# 构建训练器的方法
from modelscope.utils.constant import ModelFile

finetune_cfg = \
    {
        # 指定训练使用pytorch，无需修改
        'framework': 'pytorch', 
        # 训练多模态表征任务（中文CLIP所支持的任务），无需修改
        'task': 'multi-modal-embedding', 
        # pipeline为多模态表征，无需修改
        'pipeline': {'type': 'multi-modal-embedding'}, 
        # 使用的模型规模（以base为例），参见3.2和附录
        'pretrained_model': {'model_name': \
            'damo/multi-modal_clip-vit-base-patch16_zh'}, 
        # 图片和文本在数据集的字段名，这里以MUGE为例
        'dataset': {'column_map': {'img': 'image', 'text': 'query'}}, 
        # 模型和训练日志存储目录，最终ckpt将存放于$work_dir/output/目录
        'train': {'work_dir': './workspace/ckpts/clip', 
                # 多卡训练请解除下面这行注释，单卡保留
                # 'launcher': 'pytorch',
                # 训练轮数
                'max_epochs': 1,
                # 使用混合精度训练，无需修改
                'use_fp16': True,
                # 训练单卡batch size，根据显存实际情况决定
                'dataloader': {'batch_size_per_gpu': 180,
                                # 训练DataLoader使用进程数，0代表直接主进程读取数据
                                'workers_per_gpu': 0,
                                # 是否shuffle，无需修改
                                'shuffle': True,
                                # 丢弃每轮不够整batch的末尾数据，无需修改
                                'drop_last': True},
                # 指定学习率warmup的过程占总步数的比例
                'lr_scheduler': {'warmup_proportion': 0.1},
                # 使用学习率scheduler（cosine scheduler），无需修改
                'lr_scheduler_hook': {'type': 'LrSchedulerHook', 'by_epoch': False},
                # 优化器类型
                'optimizer': {'type': 'AdamW'},
                # 指定峰值学习率（warmup到峰值后最终decay到0）
                'optimizer_hparams': {'lr': 2.5e-05, 
                                        # 指定weight_decay，无需修改
                                        'weight_decay': 0.001, 
                                        # adam的超参，一般无需修改
                                        'beta1': 0.9, 
                                        'beta2': 0.999,
                                        'eps': 1e-08},
                # 混合精度训练相关超参，一般无需修改
                'optimizer_hook': {'type': 'TorchAMPOptimizerHook',
                                    'cumulative_iters': 1,
                                    'loss_keys': 'loss'},
                # 多卡训练时，是否通过gpu通信，在global batch上计算对比学习loss，单卡不起作用
                'loss_cfg': {'aggregate': True},
                # 每隔多少步保存一组验证指标最优的参数
                'hooks': [{'type': 'BestCkptSaverHook',
                            # 中文CLIP finetune使用in-batch 文到图检索Recall@1
                            #（注意和全局文到图检索Recall@1指标不同，仅在batch内部计算Recall）
                            'metric_key': 'inbatch_t2i_recall_at_1',
                            'by_epoch': False,
                            'interval': 200},
                            {'type': 'TextLoggerHook', 'interval': 1},
                            {'type': 'IterTimerHook'},
                            # 评测间隔，可按照步数和轮数间隔指定
                            {'type': 'EvaluationHook', 'by_epoch': False, 'interval': 200},
                            {'type': 'EvaluationHook', 'by_epoch': True, 'interval': 1},
                            {'type': 'ClipClampLogitScaleHook'}]},
        # 验证时，计算in-batch 文到图检索Recall@1使用的batch size
        'evaluation': {'dataloader': {'batch_size_per_gpu': 128,
                                    # 验证数据DataLoader使用进程数，0代表直接主进程读取数据
                                    'workers_per_gpu': 16,
                                    'shuffle': False,
                                    'drop_last': True},
                    # 中文CLIP finetune使用in-batch 文到图检索Recall@1，无需修改
                    'metrics': [{'type': 'inbatch_recall'}]},
        'preprocessor': []}


if __name__ == "__main__":
    # 初始化输出目录，请和上面dict使用相同路径
    WORKSPACE = './workspace/ckpts/clip'
    os.makedirs(WORKSPACE, exist_ok=True)
    config_file = os.path.join(WORKSPACE, ModelFile.CONFIGURATION)
    with open(config_file, 'w') as writer:
        json.dump(finetune_cfg, writer) # 保存训练超参

    # 指定预训练使用的CLIP规模，请和上面dict的'pretrained_model'保持一致
    pretrained_model = 'damo/multi-modal_clip-vit-base-patch16_zh'
    # pretrained_model = "~/.cache/modelscope/hub/damo/multi-modal_clip-vit-base-patch16_zh"
    args = dict(
        model=pretrained_model,
        work_dir=WORKSPACE,
        # 获取集成的MUGE数据集，脚本第一次执行时自动下载
        train_dataset=MsDataset.load('muge', namespace='modelscope', split='train'),
        eval_dataset=MsDataset.load('muge', namespace='modelscope', split='validation'),
        # CLIP验证时使用的指标，无需修改
        metrics=[Metrics.inbatch_recall],
        # 传入3.3.1定义的dict
        cfg_file=config_file)
    # 构建训练器
    trainer = build_trainer(name=Trainers.clip_multi_modal_embedding, default_args=args)
    # 启动训练
    trainer.train()
