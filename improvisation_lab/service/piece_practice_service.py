"""Service for practicing melodies."""

from improvisation_lab.config import Config
from improvisation_lab.domain.composition import PhraseData
from improvisation_lab.service.base_practice_service import BasePracticeService


class PiecePracticeService(BasePracticeService):
    """Service for generating and processing melodies."""

    def __init__(self, config: Config):
        """Initialize PiecePracticeService with configuration."""
        super().__init__(config)

    def generate_melody(self) -> list[PhraseData]:
        """Generate a melody based on the configured chord progression.

        Returns:
            List of PhraseData instances representing the generated melody.
        """
        selected_progression = self.config.piece_practice.chord_progressions[
            self.config.piece_practice.selected_song
        ]
        return self.melody_composer.generate_phrases(selected_progression)
