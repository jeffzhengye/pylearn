import asyncio
import json
import logging
import os
import queue
import threading
import time
import gradio as gr

import pyaudio

from cozepy import (
    COZE_CN_BASE_URL,
    AsyncCoze,
    AsyncWebsocketsChatClient,
    AsyncWebsocketsChatEventHandler,
    ChatUpdateEvent,
    ConversationAudioDeltaEvent,
    ConversationChatCompletedEvent,
    ConversationChatCanceledEvent,
    InputAudio,
    InputAudioBufferAppendEvent,
    TokenAuth,
    setup_logging,
)

# 音频参数设置
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 24000
INPUT_BLOCK_TIME = 0.05  # 50ms per block


class ModernAudioChatGUI:
    def __init__(self):
        # 初始化Coze客户端
        self.coze = AsyncCoze(
            auth=TokenAuth(os.getenv("COZE_API_TOKEN")),
            base_url=os.getenv("COZE_API_BASE", COZE_CN_BASE_URL),
        )

        # 创建事件循环
        self.loop = asyncio.new_event_loop()
        self.chat_client: AsyncWebsocketsChatClient = None

        # 初始化PyAudio
        self.p = pyaudio.PyAudio()
        self.recording = False
        self.stream = None
        self.audio_queue = queue.Queue()

        # 添加音频播放队列
        self.playback_queue = queue.Queue()
        self.is_playing = False
        self.playback_stream = None

        # 启动异步事件循环
        threading.Thread(target=self.run_async_loop, daemon=True).start()

    def start_chat(self):
        self.start_recording()
        return "开始新的对话"

    def end_chat(self):
        if self.recording:
            self.stop_recording()
        if self.chat_client:
            asyncio.run_coroutine_threadsafe(self.close_connection(), self.loop)
        return "对话已结束"

    def close_connection(self):
        async def close():
            if self.chat_client:
                await self.chat_client.close()
                self.chat_client = None

        return close()

    def start_recording(self):
        try:
            self.recording = True

            # 计算输入缓冲区大小
            input_frames_per_block = int(RATE * INPUT_BLOCK_TIME)

            # 打开音频流
            self.stream = self.p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=input_frames_per_block,
                stream_callback=self.audio_callback,
            )

            # 启动WebSocket连接
            self.loop.call_soon_threadsafe(self.start_websocket_connection)

        except Exception as e:
            print(f"启动录音错误: {e}")
            self.recording = False

    def audio_callback(self, in_data, frame_count, time_info, status):
        if self.recording:
            try:
                self.audio_queue.put(in_data)
            except Exception as e:
                print(f"录音回调错误: {e}")
        return (None, pyaudio.paContinue)

    def stop_recording(self):
        try:
            self.recording = False
            if self.stream is not None and self.stream.is_active():
                self.stream.stop_stream()
                self.stream.close()
            self.stream = None
        except Exception as e:
            print(f"停止录音错误: {e}")
        finally:
            self.stream = None

    def run_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def start_websocket_connection(self):
        async def start():
            class ChatEventHandler(AsyncWebsocketsChatEventHandler):
                def __init__(self, gui):
                    self.gui = gui
                    self.is_first_audio = True
                    self.temp_file = open("temp_response.pcm", "wb")

                async def on_conversation_audio_delta(
                    self, cli: AsyncWebsocketsChatClient, event: ConversationAudioDeltaEvent
                ):
                    try:
                        audio_data = event.data.get_audio()
                        if audio_data:
                            # 写入临时文件
                            self.temp_file.write(audio_data)
                            self.temp_file.flush()

                            # 如果是第一块音频数据，开始播放
                            if self.is_first_audio:
                                self.is_first_audio = False
                                self.gui.start_streaming_playback()

                            # 将音频数据放入播放队列
                            self.gui.playback_queue.put(audio_data)
                    except Exception as e:
                        print(f"处理音频数据错误: {e}")

                async def on_conversation_chat_completed(
                    self, cli: AsyncWebsocketsChatClient, event: ConversationChatCompletedEvent
                ):
                    try:
                        # 关闭临时文件
                        self.temp_file.close()

                        # 标记播放结束
                        self.gui.playback_queue.put(None)

                        # 重新开始录音
                        self.gui.start_recording()
                    except Exception as e:
                        print(f"完成对话错误: {e}")

                async def on_conversation_chat_canceled(
                    self, cli: AsyncWebsocketsChatClient, event: ConversationChatCanceledEvent
                ):
                    try:
                        print("打断")
                    except Exception as e:
                        print(f"对话打断错误: {e}")

            kwargs = json.loads(os.getenv("COZE_KWARGS") or "{}")
            self.chat_client = self.coze.websockets.chat.create(
                bot_id=os.getenv("COZE_BOT_ID"),
                on_event=ChatEventHandler(self),
                **kwargs,
            )

            async with self.chat_client() as client:
                await client.chat_update(
                    ChatUpdateEvent.Data.model_validate(
                        {
                            "input_audio": InputAudio.model_validate(
                                {
                                    "format": "pcm",
                                    "sample_rate": RATE,
                                    "channel": CHANNELS,
                                    "bit_depth": 16,
                                    "codec": "pcm",
                                }
                            ),
                        }
                    )
                )
                while self.chat_client:
                    if not self.audio_queue.empty():
                        audio_data = self.audio_queue.get()
                        await client.input_audio_buffer_append(
                            InputAudioBufferAppendEvent.Data.model_validate(
                                {
                                    "delta": audio_data,
                                }
                            )
                        )
                    await asyncio.sleep(0.1)

        asyncio.run_coroutine_threadsafe(start(), self.loop)

    def start_streaming_playback(self):
        self.is_playing = True

    def playback_loop(self):
        while True:
            try:
                if self.is_playing:
                    # 从队列中获取音频数据
                    audio_data = self.playback_queue.get()

                    # None 表示播放结束
                    if audio_data is None:
                        if self.playback_stream:
                            self.playback_stream.stop_stream()
                            self.playback_stream.close()
                            self.playback_stream = None
                        self.is_playing = False
                        continue

                    # 创建播放流（如果还没有创建）
                    if not self.playback_stream:
                        self.playback_stream = self.p.open(
                            format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK
                        )

                    # 播放音频数据
                    self.playback_stream.write(audio_data)

            except Exception as e:
                print(f"播放错误: {e}")
                self.is_playing = False
                if self.playback_stream:
                    try:
                        self.playback_stream.stop_stream()
                        self.playback_stream.close()
                    except Exception as e:
                        pass
                    self.playback_stream = None

            # 短暂休眠以避免CPU过载
            time.sleep(0.001)

    def send_audio(self):
        # 停止录音
        self.stop_recording()

        # 发送完成事件
        self.loop.call_soon_threadsafe(self.complete_audio)
        return "发送语音消息"

    def complete_audio(self):
        async def complete():
            while not self.audio_queue.empty():
                await asyncio.sleep(0.1)
            if self.chat_client:
                await self.chat_client.input_audio_buffer_complete()
                await self.chat_client.wait()

        asyncio.run_coroutine_threadsafe(complete(), self.loop)


def main():
    gui = ModernAudioChatGUI()

    with gr.Blocks() as demo:
        gr.Markdown("智能语音助手")
        chat_output = gr.Textbox(label="聊天记录", lines=10, interactive=False)
        with gr.Row():
            start_button = gr.Button("开启通话")
            send_button = gr.Button("发送", interactive=False)
            end_button = gr.Button("结束", interactive=False)

        def start_chat_fn():
            message = gui.start_chat()
            send_button.update(interactive=True)
            end_button.update(interactive=True)
            start_button.update(interactive=False)
            return f"AI: {message}"

        def send_audio_fn():
            message = gui.send_audio()
            send_button.update(interactive=False)
            return f"你: {message}"

        def end_chat_fn():
            message = gui.end_chat()
            send_button.update(interactive=False)
            end_button.update(interactive=False)
            start_button.update(interactive=True)
            return f"AI: {message}"

        start_button.click(start_chat_fn, outputs=chat_output)
        send_button.click(send_audio_fn, outputs=chat_output)
        end_button.click(end_chat_fn, outputs=chat_output)

    demo.launch()


if __name__ == "__main__":
    main()
