"""Tests for the ConsoleMelodyPracticeApp class."""

from unittest.mock import Mock, patch

import pytest

from improvisation_lab.application.piece_practice.console_piece_app import \
    ConsolePiecePracticeApp
from improvisation_lab.config import Config
from improvisation_lab.infrastructure.audio import DirectAudioProcessor
from improvisation_lab.presentation.piece_practice.console_piece_view import \
    ConsolePiecePracticeView
from improvisation_lab.service import PiecePracticeService


class TestConsolePiecePracticeApp:
    @pytest.fixture
    def init_module(self):
        """Initialize ConsolePiecePracticeApp for testing."""
        config = Config()
        service = PiecePracticeService(config)
        self.app = ConsolePiecePracticeApp(service, config)
        self.app.ui = Mock(spec=ConsolePiecePracticeView)
        self.app.audio_processor = Mock(spec=DirectAudioProcessor)
        self.app.audio_processor.is_recording = False

    @pytest.mark.usefixtures("init_module")
    @patch.object(DirectAudioProcessor, "start_recording", return_value=None)
    @patch("time.sleep", side_effect=KeyboardInterrupt)
    def test_launch(self, mock_start_recording, mock_sleep):
        """Test launching the application.

        Args:
            mock_start_recording: Mock object for start_recording method.
            mock_sleep: Mock object for sleep method.
        """
        self.app.launch()
        assert self.app.is_running
        assert self.app.current_phrase_idx == 0
        assert self.app.current_note_idx == 0
        self.app.ui.launch.assert_called_once()
        self.app.ui.display_phrase_info.assert_called_once_with(0, self.app.phrases)
        mock_start_recording.assert_called_once()

    @pytest.mark.usefixtures("init_module")
    def test_process_audio_callback(self):
        """Test processing audio callback."""
        audio_data = Mock()
        self.app.phrases = [Mock(notes=["C", "E", "G"]), Mock(notes=["C", "E", "G"])]
        self.app.current_phrase_idx = 0
        self.app.current_note_idx = 2

        with patch.object(
            self.app.service, "process_audio", return_value=Mock(remaining_time=0)
        ) as mock_process_audio:
            self.app._process_audio_callback(audio_data)
            mock_process_audio.assert_called_once_with(audio_data, "G")
            self.app.ui.display_pitch_result.assert_called_once()
            self.app.ui.display_phrase_info.assert_called_once_with(1, self.app.phrases)

    @pytest.mark.usefixtures("init_module")
    def test_advance_to_next_note(self):
        """Test advancing to the next note."""
        self.app.phrases = [Mock(notes=["C", "E", "G"])]
        self.app.current_phrase_idx = 0
        self.app.current_note_idx = 2

        self.app._advance_to_next_note()
        assert self.app.current_note_idx == 0
        assert self.app.current_phrase_idx == 0
        self.app.ui.display_phrase_info.assert_called_once_with(0, self.app.phrases)
