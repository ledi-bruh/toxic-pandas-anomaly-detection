from typing import Optional
import numpy as np


class SoundReader:
    def read_batch(self) -> Optional[np.ndarray]:
        raise NotImplementedError
