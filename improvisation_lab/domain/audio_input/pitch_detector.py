"""PitchDetector class for real-time pitch detection using FCPE."""

import numpy as np
import torch
from torchfcpe import spawn_bundled_infer_model


class PitchDetector:
    """Class for real-time pitch detection using FCPE."""

    def __init__(
        self,
        sample_rate: int = 44100,
        hop_length: int = 512,
        decoder_mode: str = "local_argmax",
        threshold: float = 0.006,
        f0_min: int = 80,
        f0_max: int = 880,
        interp_uv: bool = False,
        device: str = "cpu",
    ):
        """Initialize pitch detector.

        Args:
            sample_rate: Audio sample rate (default: 44100)
            hop_length: Number of samples between frames (default: 512)
            decoder_mode: Mode for decoder (default: "local_argmax")
            threshold: Threshold for V/UV decision (default: 0.006)
            f0_min: Minimum pitch in Hz (default: 80)
            f0_max: Maximum pitch in Hz (default: 880)
            interp_uv: Interpolate unvoiced frames (default: False)
            device: Device to run model on (default: "cpu")
        """
        self.sample_rate = sample_rate
        self.hop_length = hop_length
        self.decoder_mode = decoder_mode
        self.threshold = threshold
        self.f0_min = f0_min
        self.f0_max = f0_max
        self.interp_uv = interp_uv
        self.model = spawn_bundled_infer_model(device=device)

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
