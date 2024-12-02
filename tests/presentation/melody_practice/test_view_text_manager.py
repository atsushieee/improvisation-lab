"""Tests for the ViewTextManager class."""

import pytest

from improvisation_lab.domain.composition import PhraseData
from improvisation_lab.presentation.melody_practice.view_text_manager import \
    ViewTextManager
from improvisation_lab.service.melody_practice_service import PitchResult


class TestViewTextManager:

    @pytest.fixture
    def init_module(self):
        self.text_manager = ViewTextManager()

    @pytest.mark.usefixtures("init_module")
    def test_initialize_text(self):
        self.text_manager.initialize_text()
        assert self.text_manager.phrase_text == "No phrase data"
        assert self.text_manager.result_text == "Ready to start... (waiting for audio)"

    @pytest.mark.usefixtures("init_module")
    def test_terminate_text(self):
        self.text_manager.terminate_text()
        assert self.text_manager.phrase_text == "Session Stopped"
        assert self.text_manager.result_text == "Practice ended"

    @pytest.mark.usefixtures("init_module")
    def test_set_waiting_for_audio(self):
        self.text_manager.set_waiting_for_audio()
        assert self.text_manager.result_text == "Waiting for audio..."

    @pytest.mark.usefixtures("init_module")
    def test_update_pitch_result(self):
        pitch_result = PitchResult(
            target_note="C", current_base_note="A", is_correct=False, remaining_time=2.5
        )
        self.text_manager.update_pitch_result(pitch_result)
        assert (
            self.text_manager.result_text
            == "Target: C | Your note: A | Remaining: 2.5s"
        )

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
