"""Console-based interval practice view.

This module provides a console interface for visualizing
and interacting with interval practice sessions.
"""

from improvisation_lab.presentation.console_view import ConsolePracticeView
from improvisation_lab.presentation.interval_practice.interval_view_text_manager import \
    IntervalViewTextManager  # noqa: E501


class ConsoleIntervalPracticeView(ConsolePracticeView):
    """Console-based implementation of interval visualization."""

    def __init__(self, text_manager: IntervalViewTextManager):
        """Initialize the console view with a text manager.

        Args:
            text_manager: Text manager for updating and displaying text.
        """
        super().__init__(text_manager)

    def launch(self):
        """Run the console interface."""
        print("Interval Practice: ")
        print("Sing each note for 1 second!")
