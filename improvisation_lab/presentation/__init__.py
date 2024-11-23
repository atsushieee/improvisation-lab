"""Presentation layer for the application."""

from improvisation_lab.presentation.melody_view import NoteDisplay
from improvisation_lab.presentation.console_view import ConsoleView
from improvisation_lab.presentation.web_interface_view import WebInterfaceView

__all__ = ["ConsoleView", "WebInterfaceView", "NoteDisplay"]
