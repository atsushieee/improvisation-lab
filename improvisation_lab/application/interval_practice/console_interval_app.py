"""Console application for interval practice."""

from typing import List

from improvisation_lab.application.base_console_app import \
    ConsoleBasePracticeApp
from improvisation_lab.config import Config
from improvisation_lab.domain.music_theory import Notes
from improvisation_lab.presentation.interval_practice import (
    ConsoleIntervalPracticeView, IntervalViewTextManager)
from improvisation_lab.service import IntervalPracticeService


class ConsoleIntervalPracticeApp(ConsoleBasePracticeApp):
    """Console application class for interval practice."""

    def __init__(self, service: IntervalPracticeService, config: Config):
        """Initialize the application using console UI.

        Args:
            service: IntervalPracticeService instance.
            config: Config instance.
        """
        super().__init__(service, config)
        self.text_manager = IntervalViewTextManager()
        self.ui = ConsoleIntervalPracticeView(self.text_manager)

    def _get_current_note(self) -> str:
        """Return the current note to be processed.

        Returns:
            The current note to be processed.
        """
        return self.phrases[self.current_phrase_idx][self.current_note_idx].value

    def _get_current_phrase(self) -> List[Notes]:
        """Return the current phrase to be processed."""
        return self.phrases[self.current_phrase_idx]

    def _generate_melody(self) -> List[List[Notes]]:
        """Generate melody specific to the practice type.

        Returns:
            The generated melody.
        """
        return self.service.generate_melody(
            num_notes=self.config.interval_practice.num_problems,
            interval=self.config.interval_practice.interval,
        )
