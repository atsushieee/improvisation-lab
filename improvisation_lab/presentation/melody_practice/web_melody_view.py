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
        on_generate_melody: Callable[[], tuple[str, str]],
        on_end_practice: Callable[[], tuple[str, str]],
        on_audio_input: Callable[[Any], tuple[str, str]],
        song_name: str,
    ):
        """Initialize the UI with callback functions.

        Args:
            on_generate_melody: Function to call when start button is clicked
            on_end_practice: Function to call when stop button is clicked
            on_audio_input: Function to process audio input
            song_name: Name of the song to be practiced
        """
        self.on_generate_melody = on_generate_melody
        self.on_end_practice = on_end_practice
        self.on_audio_input = on_audio_input
        self.song_name = song_name

    def _build_interface(self) -> gr.Blocks:
        """Create and configure the Gradio interface.

        Returns:
            gr.Blocks: The Gradio interface.
        """
        with gr.Blocks() as app:
            self._add_header()
            self.generate_melody_button = gr.Button("Generate Melody")
            with gr.Row():
                self.phrase_info_box = gr.Textbox(label="Phrase Information", value="")
                self.pitch_result_box = gr.Textbox(label="Pitch Result", value="")
            self._add_audio_input()
            self.end_practice_button = gr.Button("End Practice")

            self._add_buttons_callbacks()

        return app

    def _add_header(self):
        """Create the header section of the UI."""
        gr.Markdown(f"# {self.song_name} Melody Practice\nSing each note for 1 second!")

    def _add_buttons_callbacks(self):
        """Create the control buttons section."""
        # Connect button callbacks
        self.generate_melody_button.click(
            fn=self.on_generate_melody,
            outputs=[self.phrase_info_box, self.pitch_result_box],
        )

        self.end_practice_button.click(
            fn=self.on_end_practice,
            outputs=[self.phrase_info_box, self.pitch_result_box],
        )

    def _add_audio_input(self):
        """Create the audio input section."""
        audio_input = gr.Audio(
            label="Audio Input",
            sources=["microphone"],
            streaming=True,
            type="numpy",
            show_label=True,
        )

        # Attention: have to specify inputs explicitly,
        # otherwise the callback function is not called
        audio_input.stream(
            fn=self.on_audio_input,
            inputs=audio_input,
            outputs=[self.phrase_info_box, self.pitch_result_box],
            show_progress=False,
            stream_every=0.1,
        )

    def launch(self, **kwargs):
        """Launch the Gradio application.

        Args:
            **kwargs: Additional keyword arguments for the launch method.
        """
        app = self._build_interface()
        app.queue()
        app.launch(**kwargs)
