"""Tests for the web interface view."""

from unittest.mock import MagicMock

import pytest

from improvisation_lab.presentation.melody_view import NoteDisplay
from improvisation_lab.presentation.web_interface_view import WebInterfaceView


class TestWebInterfaceView:
    """Tests for the web interface view."""

    def setup_module(self):
        """Common setup for test module."""
        self.mock_gr = MagicMock()
        self.mock_gr.Blocks.return_value.__enter__.return_value = self.mock_gr.interface
        self.mock_gr.Row.return_value.__enter__.return_value = None
        self.view = WebInterfaceView(gradio_module=self.mock_gr)

    @pytest.fixture
    def init_module(self):
        """Initialize test module and run interface."""
        self.setup_module()
        self.view.run("test_song")

    @pytest.fixture
    def init_module_without_run(self):
        """Initialize test module without running interface."""
        self.setup_module()

    @pytest.mark.usefixtures("init_module_without_run")
    def test_create_interface(self):
        """Test create interface."""
        interface = self.view._create_interface("test_song")
        assert interface == self.mock_gr.interface
        assert self.mock_gr.Blocks.called
        assert self.mock_gr.Textbox.call_count == 2
        assert self.mock_gr.Audio.called

    @pytest.mark.usefixtures("init_module_without_run")
    def test_run(self):
        """Test run."""
        self.view.run("test_song")

        self.mock_gr.interface.queue.assert_called_once()
        self.mock_gr.interface.launch.assert_called_once_with(share=False, debug=False)

    @pytest.mark.usefixtures("init_module")
    def test_display_phrase_info(self):
        """Test display of phrase information."""
        self.view.display_phrase_info(1, "Cmaj7", "C major", ["C", "E", "G"], True)
        assert self.view.current_phrase_info == "Phrase1 (Cmaj7, C major):\nC -> E -> G"
        self.mock_gr.Textbox.return_value.update.assert_called_with(
            value=self.view.phrase_info
        )

    @pytest.mark.usefixtures("init_module")
    def test_display_next_phrase_info(self):
        """Test display of next phrase information."""
        self.view.display_next_phrase_info("Cmaj7", "C", True)
        assert self.view.next_phrase_info == "Next: Cmaj7 (C)"
        self.mock_gr.Textbox.return_value.update.assert_called_with(
            value=self.view.phrase_info
        )

    @pytest.mark.usefixtures("init_module")
    def test_display_note_status(self):
        """Test display of note status."""
        note_info = NoteDisplay(target_note="A", current_note="C", remaining_time=0.5)
        self.view.display_note_status(note_info)
        expected_status = "Target: A     | Your note: C          | Remaining: 0.5s"
        assert self.view.note_status == expected_status
        self.mock_gr.Textbox.return_value.update.assert_called_with(
            value=self.view.note_status
        )

    @pytest.mark.usefixtures("init_module")
    def test_display_practice_end(self):
        """Test display of practice end."""
        self.view.display_practice_end()
        assert self.view.phrase_info == "Stopping..."
        self.mock_gr.Textbox.return_value.update.assert_called_with(
            value=self.view.phrase_info
        )
