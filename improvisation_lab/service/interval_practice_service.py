"""Service for interval practice."""

from random import sample
from typing import List

from improvisation_lab.config import Config
from improvisation_lab.domain.music_theory import Notes
from improvisation_lab.service.base_practice_service import BasePracticeService


class IntervalPracticeService(BasePracticeService):
    """Service for interval practice."""

    def __init__(self, config: Config):
        """Initialize IntervalPracticeService with configuration."""
        super().__init__(config)

    def generate_melody(
        self, num_notes: int = 10, interval: int = 1
    ) -> List[List[Notes]]:
        """Generate a melody based on interval transitions.

        Args:
            num_notes: Number of base notes to generate. Default is 10.
            interval: Interval to move to and back. Default is 1 (semitone).

        Returns:
            List of Notes objects containing the generated melodic phrases.
        """
        base_notes = sample(list(Notes), num_notes)
        return self.melody_composer.generate_interval_melody(base_notes, interval)
