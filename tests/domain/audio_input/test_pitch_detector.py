import numpy as np
import pytest

from improvisation_lab.domain.audio_input.pitch_detector import PitchDetector


class TestPitchDetector:

    @pytest.fixture
    def init_module(self) -> None:
        """Initialization."""
        self.pitch_detector = PitchDetector()

    @pytest.mark.usefixtures("init_module")
    def test_detect_pitch_sine_wave(self):
        """Test pitch detection with a simple sine wave."""
        # Create a sine wave at 440 Hz (A4 note)
        duration = 0.2  # seconds
        # Array of sr * duration equally spaced values dividing the range 0 to duration.
        t = np.linspace(0, duration, int(self.pitch_detector.sample_rate * duration))
        frequency = 440.0
        # Generates sine waves for a specified time
        audio_data = np.sin(2 * np.pi * frequency * t).astype(np.float32)

        # Detect pitch
        detected_freq = self.pitch_detector.detect_pitch(audio_data)

        # Check if detected frequency is close to 440 Hz
        assert abs(detected_freq - 440.0) < 1.5  # Allow 1.5 Hz tolerance

    def test_custom_parameters(self):
        """Test pitch detection with custom parameters."""
        detector = PitchDetector(
            sample_rate=22050,
            f0_min=100,
            f0_max=800,
            threshold=0.01,
        )
        
        duration = 0.2
        t = np.linspace(0, duration, int(detector.sample_rate * duration))
        frequency = 440.0
        audio_data = np.sin(2 * np.pi * frequency * t).astype(np.float32)

        detected_freq = detector.detect_pitch(audio_data)
        assert abs(detected_freq - 440.0) < 1.5
