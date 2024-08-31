from logging import Logger
import threading

import numpy as np

from ..core import ArrayBuffer


__all__ = ['ArrayBufferImpl']


class ArrayBufferImpl(ArrayBuffer):
    def __init__(
        self,
        logger: Logger,
        window_size: int,
        step_size: int,
        channels: int = 8,
        dtype: np.dtype = np.float32,
    ) -> None:
        self._logger = logger
        self._window_size = window_size
        self._max_size = window_size * 2
        self._step_size = step_size
        self._channels = channels
        self._dtype = dtype
        self._array_buffer = np.empty((self._channels, 0), self._dtype)
        self._lock = threading.Lock()

    def write(self, data: bytes) -> None:
        array = np.frombuffer(data, dtype=self._dtype).reshape((self._channels, -1))

        with self._lock:
            self._array_buffer = np.c_[self._array_buffer, array]
            # print('after write', self._array_buffer.shape)

    def __call__(self) -> np.ndarray | None:
        with self._lock:
            size = self._array_buffer.shape[1]
            if size < self._window_size:
                return None

            if size > self._max_size:
                self._array_buffer = self._array_buffer[:, self._max_size :]

            ret = self._array_buffer[:, : self._window_size].copy()
            self._array_buffer = self._array_buffer[:, self._step_size :]
            # print('after call', self._array_buffer.shape)

        self._logger.info('Buffer: %s', self._array_buffer.shape)
        return ret
