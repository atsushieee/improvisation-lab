import warnings
from unittest.mock import Mock, patch

import gradio as gr
import pytest

from improvisation_lab.presentation.piece_practice.web_piece_view import \
    WebPiecePracticeView


class TestWebPiecePracticeView:

    @pytest.fixture
    def init_module(self):
        self.start_callback = Mock(return_value=("Phrase Info", "Note Status"))
        self.stop_callback = Mock(return_value=("Session Stopped", "Practice ended"))
        self.audio_callback = Mock(
            return_value=("Audio Phrase Info", "Audio Note Status")
        )
        self.web_view = WebPiecePracticeView(
            on_generate_melody=self.start_callback,
            on_end_practice=self.stop_callback,
            on_audio_input=self.audio_callback,
            song_name="Test Song",
        )

    @pytest.mark.usefixtures("init_module")
    def test_build_interface(self):
        warnings.simplefilter("ignore", category=DeprecationWarning)
        app = self.web_view._build_interface()
        assert isinstance(app, gr.Blocks)

    @pytest.mark.usefixtures("init_module")
    @patch("gradio.Markdown")
    def test_create_header(self, mock_markdown):
        self.web_view._add_header()
        mock_markdown.assert_called_once_with(
            "# Test Song Melody Practice\nSing each note for 1 second!"
        )

    @pytest.mark.usefixtures("init_module")
    def test_create_status_section(self):
        self.web_view._build_interface()
        assert isinstance(self.web_view.phrase_info_box, gr.Textbox)
        assert isinstance(self.web_view.pitch_result_box, gr.Textbox)

    @pytest.mark.usefixtures("init_module")
    def test_create_control_buttons(self):
        self.web_view._build_interface()
        self.web_view.on_generate_melody()
        self.start_callback.assert_called_once()
        self.web_view.on_end_practice()
        self.stop_callback.assert_called_once()

    @pytest.mark.usefixtures("init_module")
    def test_create_audio_input(self):
        self.web_view._build_interface()
        self.web_view.on_audio_input()
        self.audio_callback.assert_called_once()

    @pytest.mark.usefixtures("init_module")
    def test_launch(self, mocker):
        mocker.patch.object(gr.Blocks, "launch", return_value=None)
        self.web_view.launch()
        gr.Blocks.launch.assert_called_once()
