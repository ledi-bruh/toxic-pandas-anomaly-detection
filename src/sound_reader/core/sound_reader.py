import numpy as np


class SoundReader:
    def read_batch(self) -> np.ndarray | None:
        raise NotImplementedError
