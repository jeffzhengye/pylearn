import pvporcupine
import pyaudio
import struct
import os
from typing import Dict, Optional, List, Tuple


class WakeWordDetector:
    """单例模式的唤醒词检测器类
    相同的唤醒词文件和参数文件只会创建一个Porcupine实例
    """
    # 类变量，用于存储不同配置的实例
    _instances: Dict[Tuple[str, str], 'WakeWordDetector'] = {}
    _lock = False  # 简单的锁机制，防止多线程问题

    def __new__(cls, keyword_path: str, model_path: str, access_key: str = "LGS5Z3le0lI4Euj3FqdH4EdmlrotxNFocu0RtZtPcx1B3f5JDHAiaQ=="):
        # 创建实例的唯一键，由keyword_path和model_path组成
        instance_key = (keyword_path, model_path)
        
        # 如果该配置的实例不存在，则创建新实例
        if instance_key not in cls._instances:
            # 简单的锁机制
            while cls._lock:
                pass
            cls._lock = True
            try:
                if instance_key not in cls._instances:  # 双重检查锁定
                    # 创建实例
                    instance = super(WakeWordDetector, cls).__new__(cls)
                    # 初始化实例属性
                    instance._initialize(keyword_path, model_path, access_key)
                    cls._instances[instance_key] = instance
            finally:
                cls._lock = False
                
        return cls._instances[instance_key]
    
    def _initialize(self, keyword_path: str, model_path: str, access_key: str):
        """初始化Porcupine实例"""
        # 检查文件是否存在
        if not os.path.exists(keyword_path):
            raise FileNotFoundError(f"未找到关键词文件: {keyword_path}")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"未找到模型参数文件: {model_path}")

        # 创建Porcupine实例
        self.porcupine: pvporcupine.Porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=[keyword_path],
            model_path=model_path,
        )
        
        # 保存相关属性
        self.keyword_path = keyword_path
        self.model_path = model_path
        self.wake_word = os.path.basename(keyword_path).split('_')[0]  # 从文件名提取唤醒词
        self.sample_rate = self.porcupine.sample_rate
        self.frame_length = self.porcupine.frame_length
        
        # 音频流相关属性
        self.pa = None
        self.audio_stream = None
    
    def detect(self, pcm_data: List[int]) -> bool:
        """检测处理好的pcm数据是否包含唤醒词
        
        Args:
            pcm_data: 预处理好的PCM音频数据
            
        Returns:
            bool: 是否检测到唤醒词
        """
        keyword_index = self.porcupine.process(pcm_data)
        return keyword_index >= 0
    
    def detect_loop(self):
        """打开音频流并循环检测唤醒词"""
        # 初始化音频流
        self._init_audio_stream()
        
        print(f"等待唤醒词...")
        print(f"唤醒词: {self.wake_word}，frame_length={self.frame_length}, sample_rate={self.sample_rate}")

        try:
            while True:
                # 读取音频数据
                pcm = self.audio_stream.read(self.frame_length)
                pcm = struct.unpack_from("h" * self.frame_length, pcm)

                # 检测唤醒词
                if self.detect(pcm):
                    print(f"检测到唤醒词: {self.wake_word}")
                    # 在这里可以触发后续操作
        
        except KeyboardInterrupt:
            print("停止监听...")
        finally:
            self._cleanup_audio_stream()
    
    def _init_audio_stream(self):
        """初始化音频流"""
        if self.pa is None:
            self.pa = pyaudio.PyAudio()
            self.audio_stream = self.pa.open(
                rate=self.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.frame_length,
            )
    
    def _cleanup_audio_stream(self):
        """清理音频流资源"""
        if self.audio_stream is not None:
            self.audio_stream.close()
            self.audio_stream = None
        
        if self.pa is not None:
            self.pa.terminate()
            self.pa = None
    
    def delete(self):
        """删除Porcupine实例并清理资源"""
        # 清理音频流
        self._cleanup_audio_stream()
        
        # 删除Porcupine实例
        if hasattr(self, 'porcupine') and self.porcupine is not None:
            self.porcupine.delete()
            self.porcupine = None
            
        # 从单例字典中移除
        instance_key = (self.keyword_path, self.model_path)
        if instance_key in self._instances:
            del self._instances[instance_key]

    @classmethod
    def delete_all_instances(cls):
        """删除所有单例实例"""
        for instance in list(cls._instances.values()):
            instance.delete()


# 便捷函数，用于创建和使用默认的唤醒词检测器
def create_default_wake_word_detector(wake_word: str = "小华佗") -> WakeWordDetector:
    """创建默认的唤醒词检测器
    
    Args:
        wake_word: 唤醒词名称，默认为"小华佗"
        
    Returns:
        WakeWordDetector: 唤醒词检测器实例
    """
    # 获取当前目录下的模型文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    keyword_path = os.path.join(current_dir, f"{wake_word}_zh_windows_v3_0_0.ppn")
    model_path = os.path.join(current_dir, "porcupine_params_zh.pv")
    
    try:
        return WakeWordDetector(keyword_path, model_path)
    except FileNotFoundError as e:
        print(f"错误: {e}")
        print("请确保以下文件在同一目录下:")
        print(f"1. 你的中文唤醒词文件 (例如: {wake_word}_zh_windows_v3_0_0.ppn)")
        print("2. 中文参数文件 (porcupine_params_zh.pv)")
        print("\n中文参数文件可以从以下地址下载:")
        print("https://github.com/Picovoice/porcupine/tree/master/lib/common")
        raise


def detect_wake_word():
    """兼容旧版的唤醒词检测函数"""
    try:
        detector = create_default_wake_word_detector()
        detector.detect_loop()
    except Exception:
        # 发生错误时不中断程序
        pass


if __name__ == "__main__":
    # 示例用法：创建默认的唤醒词检测器并开始检测
    detect_wake_word()

    # 也可以直接使用类：
    # detector = WakeWordDetector("path/to/keyword.ppn", "path/to/model.pv")
    # detector.detect_loop()