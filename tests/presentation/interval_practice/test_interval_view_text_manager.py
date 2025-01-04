"""Tests for the ViewTextManager class."""

import pytest

from improvisation_lab.domain.music_theory import Notes
from improvisation_lab.presentation.interval_practice.interval_view_text_manager import \
    IntervalViewTextManager  # noqa: E501


class TestIntervalViewTextManager:
    """Tests for the IntervalViewTextManager class."""

    @pytest.fixture
    def init_module(self):
        self.text_manager = IntervalViewTextManager()

    @pytest.mark.usefixtures("init_module")
    def test_update_phrase_text_no_phrases(self):
        result = self.text_manager.update_phrase_text(0, [])
        assert result == "No phrase data"
        assert self.text_manager.phrase_text == "No phrase data"

    @pytest.mark.usefixtures("init_module")
    def test_update_phrase_text_with_phrases(self):
        phrases = [
            [Notes.C, Notes.C_SHARP, Notes.C],
            [Notes.A, Notes.A_SHARP, Notes.A],
        ]
        self.text_manager.update_phrase_text(0, phrases)
        expected_text = "Problem 1: \nC -> C# -> C\nNext Base Note: A"
        assert self.text_manager.phrase_text == expected_text

        self.text_manager.update_phrase_text(1, phrases)
        expected_text = "Problem 2: \nA -> A# -> A"
        assert self.text_manager.phrase_text == expected_text
