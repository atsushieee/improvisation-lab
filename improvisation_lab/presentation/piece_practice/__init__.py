"""Presentation layer for piece practice.

This package contains modules for handling the user interface
and text management for piece practice applications.
"""

from improvisation_lab.presentation.piece_practice.console_piece_view import \
    ConsolePiecePracticeView
from improvisation_lab.presentation.piece_practice.piece_view_text_manager import \
    PieceViewTextManager
from improvisation_lab.presentation.piece_practice.web_piece_view import \
    WebPiecePracticeView

__all__ = ["WebPiecePracticeView", "PieceViewTextManager", "ConsolePiecePracticeView"]
