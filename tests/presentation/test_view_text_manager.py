"""Tests for the ViewTextManager class."""

from typing import List, Optional

import pytest

from improvisation_lab.presentation.view_text_manager import ViewTextManager
from improvisation_lab.service.base_practice_service import PitchResult


class MockViewTextManager(ViewTextManager):
    """Mock implementation of ViewTextManager for testing."""

    def __init__(self):
        super().__init__()

    def update_phrase_text(self, current_phrase_idx: int, phrases: Optional[List]):
        pass


class TestViewTextManager:

    @pytest.fixture
    def init_module(self):
        self.text_manager = MockViewTextManager()

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
        # Test without auto advance
        self.text_manager.update_pitch_result(pitch_result)
        assert (
            self.text_manager.result_text
            == "Target: C | Your note: A | Remaining: 2.5s"
        )

        # Test with auto advance
        self.text_manager.update_pitch_result(pitch_result, is_auto_advance=True)
        assert self.text_manager.result_text == "Target: C | Your note: A"
