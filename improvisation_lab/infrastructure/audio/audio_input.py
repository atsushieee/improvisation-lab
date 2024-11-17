"""Module providing abstract base class for audio input handling."""

from abc import ABC, abstractmethod


class AudioInput(ABC):
    """Abstract base class for audio input handling."""

    @abstractmethod
    def start_recording(self):
        """Start recording audio."""
        pass

    @abstractmethod
    def stop_recording(self):
        """Stop recording audio."""
        pass
