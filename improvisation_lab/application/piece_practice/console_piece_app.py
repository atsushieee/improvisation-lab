"""Console application for piece practice."""

from improvisation_lab.application.base_console_app import \
    ConsoleBasePracticeApp
from improvisation_lab.config import Config
from improvisation_lab.presentation.piece_practice import (
    ConsolePiecePracticeView, PieceViewTextManager)
from improvisation_lab.service import PiecePracticeService


class ConsolePiecePracticeApp(ConsoleBasePracticeApp):
    """Console application class for piece practice."""

    def __init__(self, service: PiecePracticeService, config: Config):
        """Initialize the application using console UI.

        Args:
            service: PiecePracticeService instance.
            config: Config instance.
        """
        super().__init__(service, config)
        self.text_manager = PieceViewTextManager()
        self.ui = ConsolePiecePracticeView(
            self.text_manager, config.piece_practice.selected_song
        )

    def _get_current_note(self):
        """Return the current note to be processed."""
        current_phrase = self.phrases[self.current_phrase_idx]
        return current_phrase.notes[self.current_note_idx]

    def _get_current_phrase(self):
        """Return the current phrase to be processed."""
        return self.phrases[self.current_phrase_idx].notes

    def _generate_melody(self):
        """Generate melody specific to the practice type."""
        return self.service.generate_melody()
