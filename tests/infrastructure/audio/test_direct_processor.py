from unittest.mock import Mock, patch

import numpy as np
import pyaudio
import pytest

from improvisation_lab.infrastructure.audio import DirectAudioProcessor


class TestMicInput:
    @pytest.fixture
    def init_module(self):
        self.mic_input = DirectAudioProcessor(sample_rate=44100)

    @pytest.mark.usefixtures("init_module")
    @patch("pyaudio.PyAudio")
    def test_start_recording(self, mock_pyaudio):
        """Test recording start functionality."""
        self.mic_input.start_recording()

        assert self.mic_input.is_recording
        # Verify that the PyAudio settings are correct
        mock_pyaudio.return_value.open.assert_called_once_with(
            format=pyaudio.paFloat32,
            channels=1,
            rate=44100,
            input=True,
            stream_callback=self.mic_input._audio_callback,
        )

    @pytest.mark.usefixtures("init_module")
    def test_start_recording_when_already_recording(self):
        """Test that starting recording when already recording raises RuntimeError."""
        self.mic_input.is_recording = True

        with pytest.raises(RuntimeError) as exc_info:
            self.mic_input.start_recording()

        assert str(exc_info.value) == "Recording is already in progress"

    @pytest.mark.usefixtures("init_module")
    def test_audio_callback(self):
        """Test that the audio callback is called with the correct data."""
        # Create sample audio data that matches the buffer size
        buffer_duration = 0.2
        sample_rate = 44100
        buffer_size = int(sample_rate * buffer_duration)
        test_data = np.array([0.1] * buffer_size, dtype=np.float32)
        test_bytes = test_data.tobytes()

        # Create a mock callback
        mock_callback = Mock()
        self.mic_input._callback = mock_callback

        # Call the audio callback
        result = self.mic_input._audio_callback(test_bytes, len(test_data), {}, 0)

        # Verify the callback was called with the correct data
        # First element of call_args is the first argument of the callback function
        np.testing.assert_array_almost_equal(mock_callback.call_args[0][0], test_data)

        # pyaudio.paContinue is an integer constant representing the stream status
        # 0: continue, 1: complete, 2: error
        assert result == (test_bytes, pyaudio.paContinue)

    @pytest.mark.usefixtures("init_module")
    @patch("pyaudio.PyAudio")
    def test_stop_recording(self, mock_pyaudio):
        """Test recording stop functionality."""
        # First start recording to set up the stream
        self.mic_input.start_recording()

        # Now test stopping
        self.mic_input.stop_recording()

        # Verify recording state
        assert not self.mic_input.is_recording
        assert self.mic_input._stream is None
        assert self.mic_input.audio is None

        # Verify that stream methods were called
        mock_stream = mock_pyaudio.return_value.open.return_value
        mock_stream.stop_stream.assert_called_once()
        mock_stream.close.assert_called_once()
        mock_pyaudio.return_value.terminate.assert_called_once()

    @pytest.mark.usefixtures("init_module")
    def test_stop_recording_not_recording(self):
        """Test that stopping when not recording raises an error."""
        with pytest.raises(RuntimeError, match="Recording is not in progress"):
            self.mic_input.stop_recording()

    @pytest.mark.usefixtures("init_module")
    def test_append_to_buffer(self):
        """Test appending data to the buffer."""
        initial_data = np.array([0.1, 0.2], dtype=np.float32)
        new_data = np.array([0.3, 0.4], dtype=np.float32)
        expected_data = np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32)

        self.mic_input._buffer = initial_data
        self.mic_input._append_to_buffer(new_data)

        np.testing.assert_array_almost_equal(self.mic_input._buffer, expected_data)

    @pytest.mark.usefixtures("init_module")
    def test_process_buffer(self):
        """Test processing buffer when it reaches the desired size."""
        # Setup buffer with more data than buffer_size
        buffer_size = self.mic_input._buffer_size
        test_data = np.array([0.1] * (buffer_size + 2), dtype=np.float32)
        self.mic_input._buffer = test_data

        # Setup mock callback
        mock_callback = Mock()
        self.mic_input._callback = mock_callback

        # Process buffer
        self.mic_input._process_buffer()

        # Verify callback was called with correct data
        np.testing.assert_array_almost_equal(
            mock_callback.call_args[0][0], test_data[:buffer_size]
        )

        # Verify remaining data in buffer
        np.testing.assert_array_almost_equal(
            self.mic_input._buffer, test_data[buffer_size:]
        )
