import numpy as np

from ..core import ArrayBuffer


__all__ = ['ArrayBufferImpl']


class ArrayBufferImpl(ArrayBuffer):
    def __init__(
        self,
        window_size: int,
        step_size: int,
        channels: int = 8,
        dtype: np.dtype = np.float32,
    ) -> None:
        self._window_size = window_size
        self._step_size = step_size
        self._channels = channels
        self._dtype = dtype
        self._array_buffer = np.empty((self._channels, 0), self._dtype)

    def write(self, data: bytes) -> None:
        array = np.frombuffer(data, dtype=self._dtype).reshape((self._channels, -1))

        self._array_buffer = np.c_[self._array_buffer, array]

    def __call__(self) -> np.ndarray | None:
        if self._array_buffer.shape[1] < self._window_size:
            return None

        ret = self._array_buffer[:, : self._window_size]
        self._array_buffer = self._array_buffer[:, -self._step_size :]
        return ret
