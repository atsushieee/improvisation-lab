"""Module for handling audio input through Gradio interface."""

from typing import Callable

import numpy as np
from scipy import signal

from improvisation_lab.infrastructure.audio.audio_processor import \
    AudioProcessor


class WebAudioProcessor(AudioProcessor):
    """Handle audio input from Gradio interface."""

    def __init__(
        self,
        sample_rate: int,
        callback: Callable[[np.ndarray], None] | None = None,
        buffer_duration: float = 0.3,
    ):
        """Initialize GradioAudioInput.

        Args:
            sample_rate: Audio sample rate in Hz
            callback: Optional callback function to process audio data
            buffer_duration: Duration of audio buffer in seconds
        """
        super().__init__(sample_rate, callback, buffer_duration)

    def _resample_audio(
        self, audio_data: np.ndarray, original_sr: int, target_sr: int
    ) -> np.ndarray:
        """Resample audio data to target sample rate.

        In the case of Gradio,
        the sample rate of the audio data may not match the target sample rate.

        Args:
            audio_data: numpy array of audio samples
            original_sr: Original sample rate in Hz
            target_sr: Target sample rate in Hz

        Returns:
            Resampled audio data with target sample rate
        """
        number_of_samples = round(len(audio_data) * float(target_sr) / original_sr)
        resampled_data = signal.resample(audio_data, number_of_samples)
        return resampled_data

    def _normalize_audio(self, audio_data: np.ndarray) -> np.ndarray:
        """Normalize audio data to range [-1, 1] by dividing by maximum absolute value.

        Args:
            audio_data: numpy array of audio samples

        Returns:
            Normalized audio data with values between -1 and 1
        """
        if len(audio_data) == 0:
            return audio_data
        max_abs = np.max(np.abs(audio_data))
        return audio_data if max_abs == 0 else audio_data / max_abs

    def _remove_low_amplitude_noise(self, audio_data: np.ndarray) -> np.ndarray:
        """Remove low amplitude noise from audio data.

        Applies a threshold to remove low amplitude signals that are likely noise.

        Args:
            audio_data: Audio data as numpy array

        Returns:
            Audio data with low amplitude noise removed
        """
        # [TODO] Set appropriate threshold
        threshold = 20.0
        audio_data[np.abs(audio_data) < threshold] = 0
        return audio_data

    def process_audio(self, audio_input: tuple[int, np.ndarray]) -> None:
        """Process incoming audio data from Gradio.

        Args:
            audio_input: Tuple of (sample_rate, audio_data)
                        where audio_data is a (samples, channels) array
        """
        if not self.is_recording:
            return

        input_sample_rate, audio_data = audio_input
        if input_sample_rate != self.sample_rate:
            audio_data = self._resample_audio(
                audio_data, input_sample_rate, self.sample_rate
            )
        audio_data = self._remove_low_amplitude_noise(audio_data)
        audio_data = self._normalize_audio(audio_data)

        self._append_to_buffer(audio_data)
        self._process_buffer()

    def start_recording(self):
        """Start accepting audio input from Gradio."""
        if self.is_recording:
            raise RuntimeError("Recording is already in progress")
        self.is_recording = True

    def stop_recording(self):
        """Stop accepting audio input from Gradio."""
        if not self.is_recording:
            raise RuntimeError("Recording is not in progress")
        self.is_recording = False
        self._buffer = np.array([], dtype=np.float32)
