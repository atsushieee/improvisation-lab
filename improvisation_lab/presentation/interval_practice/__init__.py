"""Presentation layer for interval practice.

This package contains modules for handling the user interface
and text management for interval practice applications.
"""

from improvisation_lab.presentation.interval_practice.console_interval_view import \
    ConsoleIntervalPracticeView
from improvisation_lab.presentation.interval_practice.interval_view_text_manager import \
    IntervalViewTextManager  # noqa: E501
from improvisation_lab.presentation.interval_practice.web_interval_view import \
    WebIntervalPracticeView

__all__ = [
    "WebIntervalPracticeView",
    "ConsoleIntervalPracticeView",
    "IntervalViewTextManager",
]
