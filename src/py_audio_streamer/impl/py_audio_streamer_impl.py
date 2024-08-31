import threading

import numpy as np
import pyaudio

from src.shared.infrastructure import ArrayBuffer
from ..core import PyAudioStreamer


__all__ = ['PyAudioStreamerImpl']


class PyAudioStreamerImpl(PyAudioStreamer):
    def __init__(
        self,
        buffer: ArrayBuffer,
        chunk_size: int,
        rate: int = 22050,
        target_channels: int = 8,
    ) -> None:
        self.buffer = buffer
        self.chunk_size = chunk_size
        self.rate = rate
        self.target_channels = target_channels

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run)

    def start_streaming(self) -> None:
        self.thread.start()

    def _run(self) -> None:
        try:
            while True:
                data = self.stream.read(self.chunk_size)
                ar = np.frombuffer(data, dtype=np.float32).reshape(1, -1).repeat(self.target_channels, axis=0)
                self.buffer.write(ar.tobytes())
        finally:
            self.stop_streaming()

    def stop_streaming(self) -> None:
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        self.stop_event.set()
        self.thread.join()
