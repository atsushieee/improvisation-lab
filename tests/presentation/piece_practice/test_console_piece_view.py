import pytest

from improvisation_lab.domain.composition import PhraseData
from improvisation_lab.presentation.piece_practice.console_piece_view import \
    ConsolePiecePracticeView
from improvisation_lab.presentation.piece_practice.piece_view_text_manager import \
    PieceViewTextManager
from improvisation_lab.service.base_practice_service import PitchResult


class TestConsolePiecePracticeView:
    """Tests for the ConsolePiecePracticeView class."""

    @pytest.fixture
    def init_module(self):
        self.text_manager = PieceViewTextManager()
        self.console_view = ConsolePiecePracticeView(self.text_manager, "Test Song")

    @pytest.mark.usefixtures("init_module")
    def test_launch(self, capsys):
        self.console_view.launch()
        captured = capsys.readouterr()
        assert "Generating melody for Test Song:" in captured.out
        assert "Sing each note for 1 second!" in captured.out

    @pytest.mark.usefixtures("init_module")
    def test_display_phrase_info(self, capsys):
        phrases_data = [
            PhraseData(
                notes=["C", "E", "G"],
                chord_name="Cmaj7",
                scale_info="C major",
                length=4,
            )
        ]
        self.console_view.display_phrase_info(0, phrases_data)
        captured = capsys.readouterr()
        assert "Phrase 1: Cmaj7" in captured.out
        assert "C -> E -> G" in captured.out

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
