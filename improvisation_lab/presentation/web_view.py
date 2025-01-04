"""Web-based piece practice view.

This module provides a web interface using Gradio for visualizing
and interacting with piece practice sessions.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Tuple

import gradio as gr
import numpy as np


class WebPracticeView(ABC):
    """Handles the user interface for all practice applications."""

    def __init__(
        self,
        on_generate_melody: Callable[..., Tuple[Any, ...]],
        on_end_practice: Callable[[], Tuple[Any, ...]],
        on_audio_input: Callable[[Tuple[int, np.ndarray]], Tuple[Any, ...]],
    ):
        """Initialize the UI with callback functions.

        Args:
            on_generate_melody: Function to call when start button is clicked
            on_end_practice: Function to call when stop button is clicked
            on_audio_input: Function to process audio input
        """
        self.on_generate_melody = on_generate_melody
        self.on_end_practice = on_end_practice
        self.on_audio_input = on_audio_input

    def launch(self, **kwargs):
        """Launch the Gradio application.

        Args:
            **kwargs: Additional keyword arguments for the launch method.
        """
        app = self._build_interface()
        app.queue()
        app.launch(**kwargs)

    @abstractmethod
    def _build_interface(self) -> gr.Blocks:
        """Create and configure the Gradio interface.

        Returns:
            gr.Blocks: The Gradio interface.
        """
        pass
