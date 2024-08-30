class ByteBufferImpl:
    def __init__(self, size):
        self.buffer = bytearray(size)
        self.size = size
        self.position = 0
        self.length = 0

    def write(self, data: bytes):
        data_len = len(data)
        if data_len + self.length > self.size:
            raise ValueError("Not enough space in buffer")
        self.buffer[self.length:self.length + data_len] = data
        self.length += data_len

    def read(self, window_size):
        if window_size > self.length:
            raise ValueError("Window exceeds buffer size")
        window = self.buffer[:window_size]
        self.buffer = self.buffer[window_size:] + bytearray(window_size)  # Сдвигаем оставшиеся данные в начало
        self.length -= window_size
        return window

    def seek(self, position):
        if position < 0 or position >= self.length:
            raise ValueError("Position out of bounds")
        self.position = position

    def reset(self):
        self.position = 0
        self.length = 0
