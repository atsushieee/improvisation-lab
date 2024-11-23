"""Module for melody visualization interfaces."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class NoteDisplay:
    """Data structure for note display information."""

    target_note: str
    current_note: str | None
    remaining_time: float | None


class MelodyView(ABC):
    """Abstract base class for melody visualization."""

    def display_practice_start(self, song_name: str):
        """Display practice session start message.

        Args:
            song_name: Name of the song being practiced
        """
        pass

    @abstractmethod
    def display_phrase_info(
        self, phrase_number: int, chord_name: str, scale_info: str, notes: list[str]
    ):
        """Display information about the current phrase.

        Args:
            phrase_number: The current phrase number
            chord_name: Name of the chord
            scale_info: Scale information
            notes: List of notes in the phrase
        """
        pass

    @abstractmethod
    def display_next_phrase_info(self, chord_name: str, first_note: str):
        """Display information about the next phrase.

        Args:
            chord_name: Name of the next chord
            first_note: First note of the next phrase
        """
        pass

    def display_singing_instruction(self):
        """Display singing instruction for the user."""
        pass

    @abstractmethod
    def display_note_status(self, note_info: NoteDisplay):
        """Display current note status.

        Args:
            note_info: Information about the current note status
        """
        pass

    @abstractmethod
    def display_practice_end(self):
        """Display practice session end message."""
        pass
