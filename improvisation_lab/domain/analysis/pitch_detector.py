"""PitchDetector class for real-time pitch detection using FCPE."""

import numpy as np
import torch
from torchfcpe import spawn_bundled_infer_model

from improvisation_lab.config import PitchDetectorConfig


class PitchDetector:
    """Class for real-time pitch detection using FCPE."""

    def __init__(self, config: PitchDetectorConfig):
        """Initialize pitch detector.

        Args:
            config: Configuration settings for pitch detection.
        """
        self.sample_rate = config.sample_rate
        self.hop_length = config.hop_length
        self.decoder_mode = config.decoder_mode
        self.threshold = config.threshold
        self.f0_min = config.f0_min
        self.f0_max = config.f0_max
        self.interp_uv = config.interp_uv
        self.model = spawn_bundled_infer_model(device=config.device)

    def detect_pitch(self, audio_frame: np.ndarray) -> float:
        """Detect pitch from audio frame.

        Args:
            audio_frame: Numpy array of audio samples

        Returns:
            Frequency in Hz
        """
        audio_length = len(audio_frame)
        f0_target_length = (audio_length // self.hop_length) + 1

        # Convert to torch tensor and reshape to match expected dimensions
        # Add batch and channel dimensions
        audio_tensor = torch.from_numpy(audio_frame).float()
        audio_tensor = audio_tensor.unsqueeze(0).unsqueeze(-1)

        pitch = self.model.infer(
            audio_tensor,
            sr=self.sample_rate,
            decoder_mode=self.decoder_mode,
            threshold=self.threshold,
            f0_min=self.f0_min,
            f0_max=self.f0_max,
            interp_uv=self.interp_uv,
            output_interp_target_length=f0_target_length,
        )

        # Extract the middle frequency value from the pitch tensor
        # Taking the middle value helps avoid potential inaccuracies at the edges
        # of the audio frame, providing a more stable frequency estimate.
        middle_index = pitch.size(1) // 2
        frequency = pitch[0, middle_index, 0].item()
        return frequency
