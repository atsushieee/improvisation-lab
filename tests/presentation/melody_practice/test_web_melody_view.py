import warnings
from unittest.mock import Mock, patch

import gradio as gr
import pytest

from improvisation_lab.presentation.melody_practice.web_melody_view import \
    WebMelodyView


class TestWebMelodyView:

    @pytest.fixture
    def init_module(self):
        self.start_callback = Mock(return_value=("Phrase Info", "Note Status"))
        self.stop_callback = Mock(return_value=("Session Stopped", "Practice ended"))
        self.audio_callback = Mock(
            return_value=("Audio Phrase Info", "Audio Note Status")
        )
        self.web_view = WebMelodyView(
            start_callback=self.start_callback,
            stop_callback=self.stop_callback,
            audio_callback=self.audio_callback,
            song_name="Test Song",
        )

    @pytest.mark.usefixtures("init_module")
    def test_create_interface(self):
        warnings.simplefilter("ignore", category=DeprecationWarning)
        app = self.web_view._create_interface()
        assert isinstance(app, gr.Blocks)

    @pytest.mark.usefixtures("init_module")
    @patch("gradio.Markdown")
    def test_create_header(self, mock_markdown):
        self.web_view._create_header()
        mock_markdown.assert_called_once_with(
            "# Test Song Melody Practice\nSing each note for 1 second!"
        )

    @pytest.mark.usefixtures("init_module")
    def test_create_status_section(self):
        self.web_view._create_interface()
        assert isinstance(self.web_view.phrase_info, gr.Textbox)
        assert isinstance(self.web_view.pitch_result, gr.Textbox)

    @pytest.mark.usefixtures("init_module")
    def test_create_control_buttons(self):
        self.web_view._create_interface()
        self.web_view.start_callback()
        self.start_callback.assert_called_once()
        self.web_view.stop_callback()
        self.stop_callback.assert_called_once()

    @pytest.mark.usefixtures("init_module")
    def test_create_audio_input(self):
        self.web_view._create_interface()
        self.web_view.audio_callback()
        self.audio_callback.assert_called_once()

    @pytest.mark.usefixtures("init_module")
    def test_launch(self, mocker):
        mocker.patch.object(gr.Blocks, "launch", return_value=None)
        self.web_view.launch()
        gr.Blocks.launch.assert_called_once()
