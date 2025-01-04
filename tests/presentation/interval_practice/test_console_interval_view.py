import pytest

from improvisation_lab.domain.music_theory import Notes
from improvisation_lab.presentation.interval_practice.console_interval_view import \
    ConsoleIntervalPracticeView
from improvisation_lab.presentation.interval_practice.interval_view_text_manager import \
    IntervalViewTextManager  # noqa: E501
from improvisation_lab.service.base_practice_service import PitchResult


class TestConsoleIntervalPracticeView:
    """Tests for the ConsoleIntervalPracticeView class."""

    @pytest.fixture
    def init_module(self):
        self.text_manager = IntervalViewTextManager()
        self.console_view = ConsoleIntervalPracticeView(self.text_manager)

    @pytest.mark.usefixtures("init_module")
    def test_launch(self, capsys):
        self.console_view.launch()
        captured = capsys.readouterr()
        assert "Interval Practice:" in captured.out
        assert "Sing each note for 1 second!" in captured.out

    @pytest.mark.usefixtures("init_module")
    def test_display_phrase_info(self, capsys):
        phrases_data = [[Notes.C, Notes.C_SHARP, Notes.C]]
        self.console_view.display_phrase_info(0, phrases_data)
        captured = capsys.readouterr()
        assert "Problem 1:" in captured.out
        assert "C -> C# -> C" in captured.out

    @pytest.mark.usefixtures("init_module")
    def test_display_pitch_result(self, capsys):
        pitch_result = PitchResult(
            target_note="C", current_base_note="A", is_correct=False, remaining_time=2.5
        )
        self.console_view.display_pitch_result(pitch_result)
        captured = capsys.readouterr()
        assert "Target: C | Your note: A | Remaining: 2.5s" in captured.out

    @pytest.mark.usefixtures("init_module")
    def test_display_practice_end(self, capsys):
        self.console_view.display_practice_end()
        captured = capsys.readouterr()
        assert "Session Stopped" in captured.out
