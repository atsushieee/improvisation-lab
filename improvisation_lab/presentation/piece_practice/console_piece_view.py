"""Console-based piece practice view.

This module provides a console interface for visualizing
and interacting with piece practice sessions.
"""

from improvisation_lab.presentation.console_view import ConsolePracticeView
from improvisation_lab.presentation.piece_practice.piece_view_text_manager import \
    PieceViewTextManager


class ConsolePiecePracticeView(ConsolePracticeView):
    """Console-based implementation of piece practice."""

    def __init__(self, text_manager: PieceViewTextManager, song_name: str):
        """Initialize the console view with a text manager and song name.

        Args:
            text_manager: Text manager for updating and displaying text.
            song_name: Name of the song to be practiced.
        """
        super().__init__(text_manager)
        self.song_name = song_name

    def launch(self):
        """Run the console interface."""
        print("\n" + f"Generating melody for {self.song_name}:")
        print("Sing each note for 1 second!")
