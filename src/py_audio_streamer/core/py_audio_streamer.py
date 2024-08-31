__all__ = ['PyAudioStreamer']


class PyAudioStreamer:
    def _run(self) -> None:
        raise NotImplementedError

    def start_streaming(self) -> None:
        raise NotImplementedError

    def stop_streaming(self) -> None:
        raise NotImplementedError
