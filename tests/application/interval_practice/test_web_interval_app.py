from unittest.mock import Mock, patch

import numpy as np
import pytest

from improvisation_lab.application.interval_practice.web_interval_app import \
    WebIntervalPracticeApp
from improvisation_lab.config import Config
from improvisation_lab.domain.music_theory import Notes
from improvisation_lab.infrastructure.audio import WebAudioProcessor
from improvisation_lab.presentation.interval_practice.web_interval_view import \
    WebIntervalPracticeView
from improvisation_lab.service import IntervalPracticeService


class TestWebIntervalPracticeApp:
    @pytest.fixture
    def init_module(self):
        """Initialize WebIntervalPracticeApp for testing."""
        config = Config()
        service = IntervalPracticeService(config)
        self.app = WebIntervalPracticeApp(service, config)
        self.app.ui = Mock(spec=WebIntervalPracticeView)
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
        audio_data = np.array([0.0])
        self.app.is_running = True
        self.app.phrases = [
            [Notes.C, Notes.C_SHARP, Notes.C],
            [Notes.D, Notes.D_SHARP, Notes.D],
        ]
        self.app.current_phrase_idx = 0
        self.app.current_note_idx = 1

        mock_result = Mock()
        mock_result.target_note = "C#"
        mock_result.current_base_note = "C#"
        mock_result.remaining_time = 0.0

        with patch.object(
            self.app.service, "process_audio", return_value=mock_result
        ) as mock_process_audio:
            self.app._process_audio_callback(audio_data)
            mock_process_audio.assert_called_once_with(audio_data, "C#")
            assert (
                self.app.text_manager.result_text
                == "Target: C# | Your note: C# | Remaining: 0.0s"
            )

    @pytest.mark.usefixtures("init_module")
    def test_handle_audio(self):
        """Test handling audio input."""
        audio_data = (48000, np.array([0.0]))
        self.app.is_running = True
        with patch.object(
            self.app.audio_processor, "process_audio", return_value=None
        ) as mock_process_audio:
            base_note, phrase_text, result_text, results_table = self.app.handle_audio(
                audio_data
            )
            mock_process_audio.assert_called_once_with(audio_data)
            assert base_note == self.app.base_note
            assert phrase_text == self.app.text_manager.phrase_text
            assert result_text == self.app.text_manager.result_text
            assert results_table == self.app.results_table

    @pytest.mark.usefixtures("init_module")
    def test_start(self):
        """Test starting the application."""
        self.app.audio_processor.is_recording = False
        with patch.object(
            self.app.audio_processor, "start_recording", return_value=None
        ) as mock_start_recording:
            base_note, phrase_text, result_text, results_table = self.app.start(
                "minor 2nd", "Up", 10, True, 1.5
            )
            mock_start_recording.assert_called_once()
            assert self.app.is_running
            assert base_note == self.app.base_note
            assert phrase_text == self.app.text_manager.phrase_text
            assert result_text == self.app.text_manager.result_text
            assert results_table == self.app.results_table

    @pytest.mark.usefixtures("init_module")
    def test_stop(self):
        """Test stopping the application."""
        self.app.audio_processor.is_recording = True
        with patch.object(
            self.app.audio_processor, "stop_recording", return_value=None
        ) as mock_stop_recording:
            base_note, phrase_text, result_text = self.app.stop()
            mock_stop_recording.assert_called_once()
            assert not self.app.is_running
            assert base_note == "-"
            assert phrase_text == self.app.text_manager.phrase_text
            assert result_text == self.app.text_manager.result_text

    @pytest.mark.usefixtures("init_module")
    @pytest.mark.parametrize(
        "detected_note, expected_result",
        [("C#", "⭕️"), ("D", "X")],  # Correct case  # Incorrect case
    )
    def test_update_results_table(self, detected_note, expected_result):
        """Test updating the results table with correct and incorrect results."""
        self.app.phrases = [[Notes.C, Notes.C_SHARP, Notes.C]]
        self.app.current_phrase_idx = 0
        self.app.current_note_idx = 1
        self.app.base_note = "C"
        self.app.text_manager.result_text = f"Target: C# | Your note: {detected_note}"

        self.app.is_auto_advance = True
        self.app.update_results_table()

        expected_entry = [1, "C", "C#", detected_note, expected_result]
        assert self.app.results_table[-1] == expected_entry
