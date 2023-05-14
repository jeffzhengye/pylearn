import soundfile as sf
import numpy as np

def read_wav(f):
    data, samplerate = sf.read(f)
    print(data.shape, data.dtype, samplerate)
    print(data[-10:], np.sum(data))


def read_wav1():
    with sf.SoundFile('BAC009S0747W0330.wav', 'r+') as f:
        print('total frame', f.frames, f.channels, f.samplerate, f.format, f.format_info)
        # while f.tell() < f.frames:
        #     pos = f.tell()
        # #     data = f.read(1024)
        #     f.seek(pos)
        # #     f.write(data * 2)



if __name__ == '__main__':
    f = "/mnt/c/code/image/hedian-demo/data/audio/录音2021-11-21/1_20211121191238.wav"
    # f = 'BAC009S0747W0330.wav'
    read_wav(f)
