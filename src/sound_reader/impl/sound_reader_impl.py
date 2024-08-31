import librosa
import numpy as np

from src.sound_reader.core.sound_reader import SoundReader


class SoundReaderImpl(SoundReader):
    def __init__(self, file_path, batch_size, sr=22050):
        self.file_path = file_path
        self.batch_size = batch_size
        self.sr = sr
        self.audio, self.sample_rate = librosa.load(file_path, sr=sr, mono=False)
        self.total_samples = len(self.audio)
        self.current_position = 0

    def read_batch(self) -> np.ndarray | None:
        if self.current_position >= self.total_samples:
            return None  # End of file

        end_position = min(self.current_position + self.batch_size, self.total_samples)
        batch = self.audio[self.current_position : end_position]
        self.current_position = end_position
        return batch

    def reset(self):
        self.current_position = 0
