"""Tests for the WebMelodyPracticeApp class."""

from unittest.mock import Mock, patch

import pytest

from improvisation_lab.application.melody_practice.web_app import \
    WebMelodyPracticeApp
from improvisation_lab.config import Config
from improvisation_lab.infrastructure.audio import WebAudioProcessor
from improvisation_lab.presentation.melody_practice.web_melody_view import \
    WebMelodyView
from improvisation_lab.service import MelodyPracticeService


class TestWebMelodyPracticeApp:
    @pytest.fixture
    def init_module(self):
        """Initialize WebMelodyPracticeApp for testing."""
        config = Config()
        service = MelodyPracticeService(config)
        self.app = WebMelodyPracticeApp(service, config)
        self.app.ui = Mock(spec=WebMelodyView)
        self.app.audio_processor = Mock(spec=WebAudioProcessor)

    @pytest.mark.usefixtures("init_module")
    def test_launch(self):
        """Test launching the application."""
        with patch.object(self.app.ui, "launch", return_value=None) as mock_launch:
            self.app.launch()
            mock_launch.assert_called_once()

    @pytest.mark.usefixtures("init_module")
    def test_process_audio_callback(self):
        """Test processing audio callback."""
        audio_data = Mock()
        self.app.is_running = True
        self.app.phrases = [Mock(notes=["C", "E", "G"]), Mock(notes=["C", "E", "G"])]
        self.app.current_phrase_idx = 0
        self.app.current_note_idx = 2

        mock_result = Mock()
        mock_result.target_note = "G"
        mock_result.current_base_note = "G"
        mock_result.remaining_time = 0.0

        with patch.object(
            self.app.service, "process_audio", return_value=mock_result
        ) as mock_process_audio:
            self.app._process_audio_callback(audio_data)
            mock_process_audio.assert_called_once_with(audio_data, "G")
            assert (
                self.app.text_manager.result_text
                == "Target: G | Your note: G | Remaining: 0.0s"
            )

    @pytest.mark.usefixtures("init_module")
    def test_handle_audio(self):
        """Test handling audio input."""
        audio_data = (48000, Mock())
        self.app.is_running = True
        with patch.object(
            self.app.audio_processor, "process_audio", return_value=None
        ) as mock_process_audio:
            phrase_text, result_text = self.app.handle_audio(audio_data)
            mock_process_audio.assert_called_once_with(audio_data)
            assert phrase_text == self.app.text_manager.phrase_text
            assert result_text == self.app.text_manager.result_text

    @pytest.mark.usefixtures("init_module")
    def test_start(self):
        """Test starting the application."""
        self.app.audio_processor.is_recording = False
        with patch.object(
            self.app.audio_processor, "start_recording", return_value=None
        ) as mock_start_recording:
            phrase_text, result_text = self.app.start()
            mock_start_recording.assert_called_once()
            assert self.app.is_running
            assert phrase_text == self.app.text_manager.phrase_text
            assert result_text == self.app.text_manager.result_text

    @pytest.mark.usefixtures("init_module")
    def test_stop(self):
        """Test stopping the application."""
        self.app.audio_processor.is_recording = True
        with patch.object(
            self.app.audio_processor, "stop_recording", return_value=None
        ) as mock_stop_recording:
            phrase_text, result_text = self.app.stop()
            mock_stop_recording.assert_called_once()
            assert not self.app.is_running
            assert phrase_text == self.app.text_manager.phrase_text
            assert result_text == self.app.text_manager.result_text
