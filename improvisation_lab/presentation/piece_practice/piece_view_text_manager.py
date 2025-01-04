"""Text management for melody practice.

This class manages the text displayed
in both the web and console versions of the melody practice.
"""

from typing import List, Optional

from improvisation_lab.domain.composition import PhraseData
from improvisation_lab.presentation.view_text_manager import ViewTextManager


class PieceViewTextManager(ViewTextManager):
    """Displayed text management for melody practice."""

    def __init__(self):
        """Initialize the text manager."""
        super().__init__()

    def update_phrase_text(
        self, current_phrase_idx: int, phrases: Optional[List[PhraseData]]
    ):
        """Update the phrase text.

        Args:
            current_phrase_idx: The index of the current phrase.
            phrases: The list of phrases.
        """
        if not phrases:
            self.phrase_text = "No phrase data"
            return self.phrase_text

        current_phrase = phrases[current_phrase_idx]
        self.phrase_text = (
            f"Phrase {current_phrase_idx + 1}: "
            f"{current_phrase.chord_name}\n"
            f"{' -> '.join(current_phrase.notes)}"
        )

        if current_phrase_idx < len(phrases) - 1:
            next_phrase = phrases[current_phrase_idx + 1]
            self.phrase_text += (
                f"\nNext: {next_phrase.chord_name} ({next_phrase.notes[0]})"
            )
