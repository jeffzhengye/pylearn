import paddle
import paddlenlp as ppnlp

clip = paddle.nn.ClipGradByValue(max=10.)
optimizer = paddle.optimizer.AdamW(learning_rate=1e-6, parameters=model.parameters())
lr_scheduler = ppnlp.transformers.CosineDecayWithWarmup(learning_rate, num_training_steps, warmup_proportion)
optimizer.step()