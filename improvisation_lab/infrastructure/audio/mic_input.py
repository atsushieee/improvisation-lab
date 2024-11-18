"""Module for handling microphone input and audio processing.

This module provides functionality for real-time audio capture from a microphone,
with support for buffering and callback-based processing of audio data.
"""

from typing import Callable

import numpy as np
import pyaudio

from improvisation_lab.infrastructure.audio.audio_input import AudioInput


class MicInput(AudioInput):
    """Handle real-time audio input from microphone.

    This class provides functionality to:
    1. Capture audio from the default microphone
    2. Buffer the incoming audio data
    3. Process the buffered data through a user-provided callback function

    The audio processing is done in chunks, with the chunk size determined by
    the buffer_duration parameter. This allows for efficient real-time
    processing of audio data, such as pitch detection.
    """

    def __init__(
        self,
        sample_rate: int,
        callback: Callable[[np.ndarray], None] | None = None,
        buffer_duration: float = 0.2,
    ):
        """Initialize MicInput.

        Args:
            sample_rate: Audio sample rate in Hz
            callback: Optional callback function to process audio data
            buffer_duration: Duration of audio buffer in seconds before processing
        """
        super().__init__(sample_rate, callback, buffer_duration)
        self.audio = None
        self._stream = None

    def _audio_callback(
        self, in_data: bytes, frame_count: int, time_info: dict, status: int
    ) -> tuple[bytes, int]:
        """Process incoming audio data.

        This callback is automatically called by PyAudio
        when new audio data is available.
        The audio data is converted to a numpy array and:
        1. Stored in the internal buffer
        2. Passed to the user-provided callback function if one exists

        Note:
            This method follows PyAudio's callback function specification.
            It must accept four arguments (in_data, frame_count, time_info, status)
            and return a tuple of (bytes, status_flag).
            These arguments are automatically provided by PyAudio
            when calling this callback.

        Args:
            in_data: Raw audio input data as bytes
            frame_count: Number of frames in the input
            time_info: Dictionary with timing information
            status: Stream status flag

        Returns:
            Tuple of (input_data, pyaudio.paContinue)
        """
        # Convert bytes to numpy array (float32 format)
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        self._append_to_buffer(audio_data)
        self._process_buffer()
        return (in_data, pyaudio.paContinue)

    def start_recording(self):
        """Start recording from microphone."""
        if self.is_recording:
            raise RuntimeError("Recording is already in progress")

        self.audio = pyaudio.PyAudio()
        self._stream = self.audio.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            input=True,
            stream_callback=self._audio_callback,
        )
        self.is_recording = True

    def stop_recording(self):
        """Stop recording from microphone."""
        if not self.is_recording:
            raise RuntimeError("Recording is not in progress")

        self._stream.stop_stream()
        self._stream.close()
        self.audio.terminate()
        self.is_recording = False
        self._stream = None
        self.audio = None
