"""Tests for GradioAudioInput class."""

from unittest.mock import Mock

import numpy as np
import pytest

from improvisation_lab.infrastructure.audio import GradioAudioInput


class TestGradioAudioInput:
    @pytest.fixture
    def init_module(self):
        """Initialize test module."""
        self.sample_rate = 44100
        self.buffer_duration = 0.2
        self.audio_input = GradioAudioInput(
            sample_rate=self.sample_rate,
            buffer_duration=self.buffer_duration,
        )

    @pytest.mark.usefixtures("init_module")
    def test_initialization(self):
        """Test initialization of GradioAudioInput."""
        assert self.audio_input.sample_rate == 44100
        assert not self.audio_input.is_recording
        assert self.audio_input._callback is None
        assert len(self.audio_input._buffer) == 0
        assert self.audio_input._buffer_size == int(44100 * 0.2)

    @pytest.mark.usefixtures("init_module")
    def test_start_recording(self):
        """Test recording start functionality."""
        self.audio_input.start_recording()
        assert self.audio_input.is_recording

    @pytest.mark.usefixtures("init_module")
    def test_start_recording_when_already_recording(self):
        """Test that starting recording when already recording raises RuntimeError."""
        self.audio_input.is_recording = True
        with pytest.raises(RuntimeError, match="Recording is already in progress"):
            self.audio_input.start_recording()

    @pytest.mark.usefixtures("init_module")
    def test_stop_recording(self):
        """Test recording stop functionality."""
        self.audio_input.is_recording = True
        self.audio_input._buffer = np.array([0.1, 0.2], dtype=np.float32)

        self.audio_input.stop_recording()

        assert not self.audio_input.is_recording
        assert len(self.audio_input._buffer) == 0

    @pytest.mark.usefixtures("init_module")
    def test_stop_recording_when_not_recording(self):
        """Test that stopping recording when not recording raises RuntimeError."""
        with pytest.raises(RuntimeError, match="Recording is not in progress"):
            self.audio_input.stop_recording()

    @pytest.mark.usefixtures("init_module")
    def test_append_to_buffer(self):
        """Test appending data to the buffer."""
        initial_data = np.array([0.1, 0.2], dtype=np.float32)
        new_data = np.array([0.3, 0.4], dtype=np.float32)
        expected_data = np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32)

        self.audio_input._buffer = initial_data
        self.audio_input._append_to_buffer(new_data)

        np.testing.assert_array_almost_equal(self.audio_input._buffer, expected_data)

    @pytest.mark.usefixtures("init_module")
    def test_process_buffer(self):
        """Test processing buffer when it reaches the desired size."""
        # Setup buffer with more data than buffer_size
        buffer_size = self.audio_input._buffer_size
        test_data = np.array([0.1] * (buffer_size + 2), dtype=np.float32)
        self.audio_input._buffer = test_data

        # Setup mock callback
        mock_callback = Mock()
        self.audio_input._callback = mock_callback

        # Process buffer
        self.audio_input._process_buffer()

        # Verify callback was called with correct data
        np.testing.assert_array_almost_equal(
            mock_callback.call_args[0][0], test_data[:buffer_size]
        )

        # Verify remaining data in buffer
        np.testing.assert_array_almost_equal(
            self.audio_input._buffer, test_data[buffer_size:]
        )

    @pytest.mark.usefixtures("init_module")
    def test_resample_audio(self):
        """Test audio resampling functionality."""
        # Create test data at 48000 Hz
        duration = 0.1  # seconds
        original_sr = 48000
        target_sr = 44100
        t = np.linspace(0, duration, int(original_sr * duration))
        test_data = np.sin(2 * np.pi * 440 * t).astype(np.float32)  # 440 Hz sine wave

        # Resample to 44100 Hz
        resampled_data = self.audio_input._resample_audio(
            test_data, original_sr, target_sr
        )

        # Check that the length is correct
        expected_length = round(len(test_data) * float(target_sr) / original_sr)
        assert len(resampled_data) == expected_length

        # Check that the data is still a float32 array
        assert resampled_data.dtype == np.float32

        # Check that the signal maintains similar characteristics
        assert np.allclose(
            np.mean(np.abs(test_data)), np.mean(np.abs(resampled_data)), rtol=0.1
        )

    @pytest.mark.usefixtures("init_module")
    def test_normalize_audio_normal_case(self):
        """Test audio normalization with non-zero data."""
        # Test data with known max value
        test_data = np.array([0.5, -1.0, 0.25], dtype=np.float32)
        normalized_data = self.audio_input._normalize_audio(test_data)

        # Check that the maximum absolute value is 1.0
        assert np.max(np.abs(normalized_data)) == 1.0
        # Check that the relative relationships are preserved
        np.testing.assert_array_almost_equal(
            normalized_data, np.array([0.5, -1.0, 0.25], dtype=np.float32)
        )

    @pytest.mark.usefixtures("init_module")
    def test_normalize_audio_empty_array(self):
        """Test audio normalization with empty array."""
        test_data = np.array([], dtype=np.float32)
        normalized_data = self.audio_input._normalize_audio(test_data)

        assert len(normalized_data) == 0
        assert normalized_data.dtype == np.float32

    @pytest.mark.usefixtures("init_module")
    def test_normalize_audio_zero_array(self):
        """Test audio normalization with array of zeros."""
        test_data = np.zeros(5, dtype=np.float32)
        normalized_data = self.audio_input._normalize_audio(test_data)

        # Should return the same array of zeros without division
        np.testing.assert_array_equal(normalized_data, test_data)
        assert normalized_data.dtype == np.float32

    @pytest.mark.usefixtures("init_module")
    def test_remove_low_amplitude_noise_normal_case(self):
        """Test noise removal with mixed amplitude signals."""
        # Test data with both high and low amplitude signals
        test_data = np.array([5.0, -25.0, 0.5, 30.0, 15.0, 1.0], dtype=np.float32)
        processed_data = self.audio_input._remove_low_amplitude_noise(test_data)

        # Values below threshold (20.0) should be zero
        expected_data = np.array([0.0, -25.0, 0.0, 30.0, 0.0, 0.0], dtype=np.float32)
        np.testing.assert_array_equal(processed_data, expected_data)

    @pytest.mark.usefixtures("init_module")
    def test_remove_low_amplitude_noise_all_below_threshold(self):
        """Test noise removal when all signals are below threshold."""
        test_data = np.array([1.0, -5.0, 0.5, 10.0, 15.0], dtype=np.float32)
        processed_data = self.audio_input._remove_low_amplitude_noise(test_data)

        # All values should be zero as they're below threshold
        expected_data = np.zeros_like(test_data)
        np.testing.assert_array_equal(processed_data, expected_data)

    @pytest.mark.usefixtures("init_module")
    def test_remove_low_amplitude_noise_empty_array(self):
        """Test noise removal with empty array."""
        test_data = np.array([], dtype=np.float32)
        processed_data = self.audio_input._remove_low_amplitude_noise(test_data)

        assert len(processed_data) == 0
        assert processed_data.dtype == np.float32
