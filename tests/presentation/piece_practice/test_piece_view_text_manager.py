"""Tests for the ViewTextManager class."""

import pytest

from improvisation_lab.domain.composition import PhraseData
from improvisation_lab.presentation.piece_practice.piece_view_text_manager import \
    PieceViewTextManager


class TestPieceViewTextManager:
    """Tests for the PieceViewTextManager class."""

    @pytest.fixture
    def init_module(self):
        self.text_manager = PieceViewTextManager()

    @pytest.mark.usefixtures("init_module")
    def test_update_phrase_text_no_phrases(self):
        result = self.text_manager.update_phrase_text(0, [])
        assert result == "No phrase data"
        assert self.text_manager.phrase_text == "No phrase data"

    @pytest.mark.usefixtures("init_module")
    def test_update_phrase_text_with_phrases(self):
        phrases = [
            PhraseData(
                notes=["C", "E", "G"],
                chord_name="Cmaj7",
                scale_info="C major",
                length=4,
            ),
            PhraseData(
                notes=["A", "C", "E"],
                chord_name="Amin7",
                scale_info="A minor",
                length=4,
            ),
        ]
        self.text_manager.update_phrase_text(0, phrases)
        expected_text = "Phrase 1: Cmaj7\nC -> E -> G\nNext: Amin7 (A)"
        assert self.text_manager.phrase_text == expected_text

        self.text_manager.update_phrase_text(1, phrases)
        expected_text = "Phrase 2: Amin7\nA -> C -> E"
        assert self.text_manager.phrase_text == expected_text
