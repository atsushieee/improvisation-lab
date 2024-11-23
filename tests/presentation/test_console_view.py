"""Tests for console visualization components."""

import pytest

from improvisation_lab.presentation.console_view import ConsoleView
from improvisation_lab.presentation.melody_view import NoteDisplay


class TestConsoleView:
    """Test class for ConsoleView."""

    @pytest.fixture
    def init_module(self):
        """Initialize test module."""
        self.view = ConsoleView()

    @pytest.mark.usefixtures("init_module")
    def test_display_practice_start(self, capsys):
        """Test display practice start.

        Args:
            capsys: Pytest fixture for capturing output.
        """
        self.view.display_practice_start("test_song")
        captured = capsys.readouterr()

        expected_output = "Generating melody for test_song:\n" + "-" * 50 + "\n"
        assert captured.out == expected_output

    @pytest.mark.usefixtures("init_module")
    def test_display_phrase_info(self, capsys):
        """Test display of phrase information.

        Args:
            capsys: Pytest fixture for capturing output.
        """
        self.view.display_phrase_info(
            phrase_number=1,
            chord_name="Cmaj7",
            scale_info="C major",
            notes=["C", "E", "G"],
        )
        captured = capsys.readouterr()
        expected_output = "\nPhrase1 (Cmaj7, C major):\n" + "C -> E -> G\n"
        assert captured.out == expected_output

    @pytest.mark.usefixtures("init_module")
    def test_display_next_phrase_info(self, capsys):
        """Test display of next phrase information.

        Args:
            capsys: Pytest fixture for capturing output.
        """
        self.view.display_next_phrase_info("Cmaj7", "C")
        captured = capsys.readouterr()
        expected_output = "Next: Cmaj7 (C)\n"
        assert captured.out == expected_output

    @pytest.mark.usefixtures("init_module")
    def test_display_singing_instruction(self, capsys):
        """Test display of singing instruction.

        Args:
            capsys: Pytest fixture for capturing output.
        """
        self.view.display_singing_instruction()
        captured = capsys.readouterr()
        assert captured.out == "Sing each note for 1 second!\n"

    @pytest.mark.usefixtures("init_module")
    def test_display_note_status_no_voice(self, capsys):
        """Test display of note status when no voice is detected.

        Args:
            capsys: Pytest fixture for capturing output.
        """
        note_info = NoteDisplay(
            target_note="A",
            current_note=None,
            remaining_time=None,
        )
        self.view.display_note_status(note_info)
        captured = capsys.readouterr()
        assert "Target: A     | Your note: ---" in captured.out

    @pytest.mark.usefixtures("init_module")
    def test_display_note_status_incorrect_pitch(self, capsys):
        """Test display of note status with incorrect pitch.

        Args:
            capsys: Pytest fixture for capturing output.
        """
        note_info = NoteDisplay(
            target_note="A",
            current_note="C",
            remaining_time=None,
        )
        self.view.display_note_status(note_info)
        captured = capsys.readouterr()
        assert "Target: A     | Your note: C" in captured.out

    @pytest.mark.usefixtures("init_module")
    def test_display_note_status_correct_pitch(self, capsys):
        """Test display of note status with correct pitch.

        Args:
            capsys: Pytest fixture for capturing output.
        """
        note_info = NoteDisplay(
            target_note="A",
            current_note="A",
            remaining_time=0.5,
        )
        self.view.display_note_status(note_info)
        captured = capsys.readouterr()
        assert "Target: A     | Your note: A          | Remaining: 0.5s" in captured.out

    @pytest.mark.usefixtures("init_module")
    def test_display_practice_end(self, capsys):
        """Test display of practice end.

        Args:
            capsys: Pytest fixture for capturing output.
        """
        self.view.display_practice_end()
        captured = capsys.readouterr()
        assert captured.out == "\nStopping...\n"
