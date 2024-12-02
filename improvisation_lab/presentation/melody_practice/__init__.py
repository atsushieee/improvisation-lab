"""Presentation layer for melody practice.

This package contains modules for handling the user interface
and text management for melody practice applications.
"""

from improvisation_lab.presentation.melody_practice.console_melody_view import \
    ConsoleMelodyView
from improvisation_lab.presentation.melody_practice.view_text_manager import \
    ViewTextManager
from improvisation_lab.presentation.melody_practice.web_melody_view import \
    WebMelodyView

__all__ = ["WebMelodyView", "ViewTextManager", "ConsoleMelodyView"]
