"""Application layer for piece practice."""

from improvisation_lab.application.piece_practice.console_piece_app import \
    ConsolePiecePracticeApp
from improvisation_lab.application.piece_practice.web_piece_app import \
    WebPiecePracticeApp

__all__ = ["ConsolePiecePracticeApp", "WebPiecePracticeApp"]
