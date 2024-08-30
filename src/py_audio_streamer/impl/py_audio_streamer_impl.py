import pyaudio
import numpy as np
from src.ByteBuffer.core.byte_buffer import ByteBuffer
from src.ByteBuffer.impl.byte_buffer_impl import ByteBufferImpl
from src.py_audio_streamer.core.py_audio_streamer import PyAudioStreamer


class PyAudioStreamerImpl(PyAudioStreamer):
    def __init__(self, buffer: ByteBuffer, rate=22050, chunk_size=22050, chanals = 8):
        self.chanals = chanals
        self.buffer = buffer
        self.rate = rate
        self.chunk_size = chunk_size
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk_size)

    def start_streaming(self):
        try:
            while True:
                data = self.stream.read(self.chunk_size)
                self.buffer.write(data * self.chanals)
        except KeyboardInterrupt:
            self.stop_streaming()

    def stop_streaming(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
