class ByteBufferImpl:
    def __init__(self):
        self.position = 0
        self.buffer = bytearray()
        self.length = 0

    def write(self, data):
        if isinstance(data, list):
            for chunk in data:
                if isinstance(chunk, bytes):
                    self.buffer.extend(chunk)
                    self.length += len(chunk)
                else:
                    raise ValueError("All elements in the list must be of type 'bytes'")
        elif isinstance(data, bytes):
            self.buffer.extend(data)
            self.length += len(data)
        else:
            raise ValueError("Data must be of type 'bytes' or 'list of bytes'")

    def read(self, window_size, num_channels):
        if window_size > self.length:
            raise ValueError("Window exceeds buffer size")

        window = self.buffer[:window_size]
        self.buffer = self.buffer[window_size:]
        self.length -= window_size

        channels = [window[i::num_channels] for i in range(num_channels)]

        return channels

    def seek(self, position):
        if position < 0 or position >= self.length:
            raise ValueError("Position out of bounds")
        self.position = position

    def reset(self):
        self.buffer = bytearray()
        self.position = 0
        self.length = 0

