import pyaudio
import wave
import librosa
import soundfile as sf
import numpy as np
audio, sample_rate = librosa.load('src/sound_reader/impl/00000006.wav', mono=False)

print(len(audio[0]))

path = 'src/sound_reader/impl/00000006.wav'

import numpy as np
import soundfile as sf

# Путь к вашему аудиофайлу
path = 'src/sound_reader/impl/00000006.wav'

# Открываем файл для чтения[]
    with sf.SoundFile(path, 'r') as f:
        byte_data = f.buffer_read(f.frames * f.channels, dtype='float32')

    # Преобразуем байты в массив numpy
    audio_data = np.frombuffer(byte_data, dtype='float32')

    # Предположим, что у вас 8 каналов
    num_channels = 8
    audio_data = audio_data.reshape(-1, num_channels)

    # Теперь у вас есть доступ к каждому каналу
    for i in range(num_channels):
        channel_data = audio_data[:, i]
        print(f"Channel {i+1} data: {len(channel_data)}")

