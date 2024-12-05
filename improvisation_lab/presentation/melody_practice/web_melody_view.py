"""Web-based melody practice view.

This module provides a web interface using Gradio for visualizing
and interacting with melody practice sessions.
"""

from typing import Any, Callable

import gradio as gr


class WebMelodyView:
    """Handles the user interface for the melody practice application."""

    def __init__(
        self,
        start_callback: Callable[[], tuple[str, str]],
        stop_callback: Callable[[], tuple[str, str]],
        audio_callback: Callable[[Any], tuple[str, str]],
        song_name: str,
    ):
        """Initialize the UI with callback functions.

        Args:
            start_callback: Function to call when start button is clicked
            stop_callback: Function to call when stop button is clicked
            audio_callback: Function to process audio input
            song_name: Name of the song to be practiced
        """
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.audio_callback = audio_callback
        self.song_name = song_name

    def _create_interface(self) -> gr.Blocks:
        """Create and configure the Gradio interface.

        Returns:
            gr.Blocks: The Gradio interface.
        """
        with gr.Blocks() as app:
            self._create_header()
            self._create_status_section()
            self._create_control_buttons()
            self._create_audio_input()

        return app

    def _create_header(self):
        """Create the header section of the UI."""
        gr.Markdown(f"# {self.song_name} Melody Practice\nSing each note for 1 second!")

    def _create_status_section(self):
        """Create the status display section."""
        with gr.Row():
            self.phrase_info = gr.Textbox(label="Phrase Information", value="")
            self.pitch_result = gr.Textbox(label="Pitch Result", value="")

    def _create_control_buttons(self):
        """Create the control buttons section."""
        with gr.Row():
            start_btn = gr.Button("Start")
            stop_btn = gr.Button("Stop")

        # Connect button callbacks
        start_btn.click(
            fn=self.start_callback, outputs=[self.phrase_info, self.pitch_result]
        )

        stop_btn.click(
            fn=self.stop_callback, outputs=[self.phrase_info, self.pitch_result]
        )

    def _create_audio_input(self):
        """Create the audio input section."""
        audio_input = gr.Audio(
            label="Audio Input",
            sources=["microphone"],
            streaming=True,
            type="numpy",
            show_label=True,
        )

        # attention: have to specify inputs explicitly, otherwise the callback function is not called
        audio_input.stream(
            fn=self.audio_callback,
            inputs=audio_input,
            outputs=[self.phrase_info, self.pitch_result],
            show_progress=False,
            stream_every=0.1,
        )

    def launch(self, **kwargs):
        """Launch the Gradio application.

        Args:
            **kwargs: Additional keyword arguments for the launch method.
        """
        app = self._create_interface()
        app.queue()
        app.launch(**kwargs)
