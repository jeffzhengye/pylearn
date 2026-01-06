from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
model = load_silero_vad()
file_path = "d:/code/image/LiveTalking/logs/users_audio_buffer_768173_1761190019.wav"
wav = read_audio(file_path)
speech_timestamps = get_speech_timestamps(
  wav,
  model,
  return_seconds=True,  # Return speech timestamps in seconds (default is samples)
)