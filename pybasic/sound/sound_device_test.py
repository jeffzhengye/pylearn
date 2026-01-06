import numpy as np
import sounddevice as sd
import time

def check_audio_devices():
    """检查音频设备"""
    print("可用的音频设备:")
    devices = sd.query_devices()
    print(devices)
    
    # 获取默认设备
    print(f"\n默认输入设备: {sd.query_devices(sd.default.device[0])}")
    print(f"默认输出设备: {sd.query_devices(sd.default.device[1])}")
    
    print(f"默认采样率: {sd.default.samplerate}")
    print(f"默认数据类型: {sd.default.dtype}")

def test_beep():
    """测试beep音播放"""
    try:
        # 检查音频设备
        check_audio_devices()
        
        # 生成440Hz的提示音（500ms，增加持续时间以便更容易听到）
        duration = 0.5  # 500ms，增加持续时间
        frequency = 440  # 440Hz
        sample_rate = 16000  # 使用标准采样率
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        beep = np.sin(2 * np.pi * frequency * t) * 0.8  # 增加音量到80%

        # 确保使用正确的数据类型
        beep = beep.astype(np.float32)
        print(f"音频数据形状: {beep.shape}, 幅度范围: [{beep.min():.3f}, {beep.max():.3f}]")
        print("播放提示音...")
        
        # 使用sounddevice播放
        sd.play(beep, samplerate=sample_rate)
        sd.wait()  # 等待播放完成
        print("提示音播放完成")
        
    except Exception as e:
        print(f"播放提示音失败: {e}")
        # 如果sounddevice播放失败，尝试使用系统提示音
        try:
            import winsound
            winsound.Beep(440, 100)  # Windows系统提示音
            print("使用系统提示音成功")
        except Exception as e2:
            print(f"系统提示音也失败: {e2}")

def test_beep_with_stream():
    """测试在已有音频流的情况下播放beep音"""
    try:
        # 创建一个输出流来播放beep音
        duration = 0.5  # 500ms，增加持续时间
        frequency = 440  # 440Hz
        sample_rate = 44100  # 使用标准采样率
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        beep = np.sin(2 * np.pi * frequency * t) * 0.8  # 增加音量
        beep = beep.astype(np.float32)  # 使用float32而不是int16
        
        print(f"通过输出流播放beep音，持续时间: {duration}s")
        
        # 使用输出流播放
        with sd.OutputStream(samplerate=sample_rate, channels=1, dtype='float32') as stream:
            stream.write(beep)
            time.sleep(duration + 0.1)  # 等待播放完成加上一点缓冲时间
        
        print("通过输出流播放beep音完成")
        
    except Exception as e:
        print(f"通过输出流播放beep音失败: {e}")

def test_simple_beep():
    """测试最简单的beep音"""
    try:
        # 使用更简单的参数
        duration = 1.0  # 1秒
        frequency = 800  # 800Hz
        sample_rate = 22050  # 中等采样率
        samples = np.arange(int(duration * sample_rate))
        beep = np.sin(2 * np.pi * frequency * samples / sample_rate) * 0.7
        
        beep = beep.astype(np.float32)
        
        print(f"播放简单beep音: {frequency}Hz, {duration}s")
        sd.play(beep, samplerate=sample_rate)
        sd.wait()
        print("简单beep音播放完成")
    except Exception as e:
        print(f"简单beep音播放失败: {e}")

if __name__ == "__main__":
    print("测试0: 检查音频设备")
    check_audio_devices()
    
    time.sleep(1)  # 等待1秒
    
    print("\n测试1: 直接使用sd.play")
    test_beep()
    
    time.sleep(1)  # 等待1秒
    
    # print("\n测试2: 使用输出流")
    # test_beep_with_stream()
    
    # time.sleep(1)  # 等待1秒
    
    # print("\n测试3: 简单beep音测试")
    # test_simple_beep()
    
    # time.sleep(1)  # 等待1秒
    
    # print("\n测试4: 使用Windows系统声音")
    # try:
    #     import winsound
    #     winsound.Beep(800, 500)  # 更高的频率和更长的持续时间
    #     print("Windows系统提示音播放成功")
    # except Exception as e:
    #     print(f"Windows系统提示音失败: {e}")
