"""Module providing abstract base class for audio input handling."""

from abc import ABC, abstractmethod
from typing import Callable

import numpy as np


class AudioProcessor(ABC):
    """Abstract base class for audio input handling."""

    def __init__(
        self,
        sample_rate: int,
        callback: Callable[[np.ndarray], None] | None = None,
        buffer_duration: float = 0.2,
    ):
        """Initialize AudioInput.

        Args:
            sample_rate: Audio sample rate in Hz
            callback: Optional callback function to process audio data
            buffer_duration: Duration of audio buffer in seconds
        """
        self.sample_rate = sample_rate
        self.is_recording = False
        self._callback = callback
        self._buffer = np.array([], dtype=np.float32)
        self._buffer_size = int(sample_rate * buffer_duration)

    def _append_to_buffer(self, audio_data: np.ndarray) -> None:
        """Append new audio data to the buffer."""
        self._buffer = np.concatenate([self._buffer, audio_data])

    def _process_buffer(self) -> None:
        """Process buffer data if it has reached the desired size."""
        if len(self._buffer) >= self._buffer_size:
            if self._callback is not None:
                self._callback(self._buffer[: self._buffer_size])
            self._buffer = self._buffer[self._buffer_size :]

    @abstractmethod
    def start_recording(self):
        """Start recording audio."""
        pass

    @abstractmethod
    def stop_recording(self):
        """Stop recording audio."""
        pass
