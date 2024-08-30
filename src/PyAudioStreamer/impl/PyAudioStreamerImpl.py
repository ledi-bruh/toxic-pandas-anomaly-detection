import pyaudio

from src.ByteBuffer.core.ByteBuffer import ByteBuffer
from src.PyAudioStreamer.core.PyAudioStreamer import PyAudioStreamer


class PyAudioStreamerImpl(PyAudioStreamer):
    def __init__(self, buffer: ByteBuffer, rate=22050, chunk_size=22050):
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
                self.buffer.write(data)
        except KeyboardInterrupt:
            self.stop_streaming()

    def stop_streaming(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()


