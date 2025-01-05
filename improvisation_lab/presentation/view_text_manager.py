"""Text management for melody practice.

This class manages the text displayed
in both the web and console versions of the melody practice.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional

from improvisation_lab.service.base_practice_service import PitchResult


class ViewTextManager(ABC):
    """Displayed text management for melody practice."""

    def __init__(self):
        """Initialize the text manager."""
        self.initialize_text()

    def initialize_text(self):
        """Initialize the text."""
        self.phrase_text = "No phrase data"
        self.result_text = "Ready to start... (waiting for audio)"

    def terminate_text(self):
        """Terminate the text."""
        self.phrase_text = "Session Stopped"
        self.result_text = "Practice ended"

    def set_waiting_for_audio(self):
        """Set the text to waiting for audio."""
        self.result_text = "Waiting for audio..."

    def update_pitch_result(
        self, pitch_result: PitchResult, is_auto_advance: bool = False
    ):
        """Update the pitch result text.

        Args:
            pitch_result: The result of the pitch detection.
            is_auto_advance:
                Whether to automatically advance to the next note.
                Default is False.
        """
        result_text = (
            f"Target: {pitch_result.target_note} | "
            f"Your note: {pitch_result.current_base_note or '---'}"
        )
        if pitch_result.current_base_note is not None and not is_auto_advance:
            result_text += f" | Remaining: {pitch_result.remaining_time:.1f}s"
        self.result_text = result_text

    @abstractmethod
    def update_phrase_text(self, current_phrase_idx: int, phrases: Optional[List[Any]]):
        """Update the phrase text.

        Args:
            current_phrase_idx: The index of the current phrase.
            phrases: The list of phrases.
        """
        pass
