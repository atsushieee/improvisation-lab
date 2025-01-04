"""Console-based piece practice view.

This module provides a console interface for visualizing
and interacting with piece practice sessions.
"""

from abc import ABC, abstractmethod
from typing import List

from improvisation_lab.domain.composition import PhraseData
from improvisation_lab.presentation.view_text_manager import ViewTextManager
from improvisation_lab.service.base_practice_service import PitchResult


class ConsolePracticeView(ABC):
    """Console-based implementation of piece practice."""

    def __init__(self, text_manager: ViewTextManager):
        """Initialize the console view with a text manager and song name.

        Args:
            text_manager: Text manager for updating and displaying text.
            song_name: Name of the song to be practiced.
        """
        self.text_manager = text_manager

    @abstractmethod
    def launch(self):
        """Run the console interface."""
        pass

    def display_phrase_info(self, phrase_number: int, phrases_data: List[PhraseData]):
        """Display phrase information in console.

        Args:
            phrase_number: Number of the phrase.
            phrases_data: List of phrase data.
        """
        self.text_manager.update_phrase_text(phrase_number, phrases_data)
        print("\n" + "-" * 50)
        print("\n" + self.text_manager.phrase_text + "\n")

    def display_pitch_result(self, pitch_result: PitchResult):
        """Display note status in console.

        Args:
            pitch_result: The result of the pitch detection.
        """
        self.text_manager.update_pitch_result(pitch_result)
        print(f"{self.text_manager.result_text:<80}", end="\r", flush=True)

    def display_practice_end(self):
        """Display practice end message in console."""
        self.text_manager.terminate_text()
        print(self.text_manager.phrase_text)
