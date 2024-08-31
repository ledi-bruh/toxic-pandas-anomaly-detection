import numpy as np


__all__ = ['ArrayBuffer']


class ArrayBuffer:
    def write(self, data: np.ndarray) -> None:
        raise NotImplementedError

    def __call__(self) -> np.ndarray | None:
        raise NotImplementedError
