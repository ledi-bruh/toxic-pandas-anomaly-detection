class ByteBuffer:
    def write(self, data: list[bytes]) -> None:
        raise NotImplementedError

    def read(self) -> bytearray:
        raise NotImplementedError

    def seek(self) -> None:
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError
