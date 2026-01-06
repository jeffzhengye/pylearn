import openwakeword
import pyaudio
import numpy as np

# 加载模型
openwakeword.utils.download_models()

# 初始化检测器，可以启用VAD和噪声抑制
owwModel = openwakeword.Model(
    # 可选：启用语音活动检测，减少误触发
    # vad_threshold=0.5,
    # 可选：在支持的平台上启用噪声抑制
    # enable_speex_noise_suppression=True
)

def detect_wake_word_openwakeword():
    # 初始化音频流
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1280
    )
    
    print("等待唤醒词...")
    
    try:
        while True:
            # 读取音频数据
            audio_data = stream.read(1280)
            audio_data = np.frombuffer(audio_data, dtype=np.int16)
            
            # 预测
            prediction = owwModel.predict(audio_data)
            
            # 检查是否有唤醒词被检测到
            for model_name, prediction_value in prediction.items():
                # 可以根据实际环境调整阈值
                if prediction_value >= 0.5:
                    print(f"检测到唤醒词: {model_name} (置信度: {prediction_value:.2f})")
                    
    except KeyboardInterrupt:
        print("停止监听...")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    detect_wake_word_openwakeword()