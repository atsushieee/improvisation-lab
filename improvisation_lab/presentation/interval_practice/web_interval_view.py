"""Web-based interval practice view.

This module provides a web interface using Gradio for visualizing
and interacting with interval practice sessions.
"""

from typing import Callable, List, Tuple

import gradio as gr
import numpy as np

from improvisation_lab.config import Config
from improvisation_lab.domain.music_theory import Intervals
from improvisation_lab.presentation.web_view import WebPracticeView


class WebIntervalPracticeView(WebPracticeView):
    """Handles the user interface for the melody practice application."""

    def __init__(
        self,
        on_generate_melody: Callable[[str, str, int], Tuple[str, str, str, List]],
        on_end_practice: Callable[[], Tuple[str, str, str]],
        on_audio_input: Callable[[Tuple[int, np.ndarray]], Tuple[str, str, str, List]],
        config: Config,
    ):
        """Initialize the UI with callback functions.

        Args:
            on_generate_melody: Function to call when start button is clicked
            on_end_practice: Function to call when stop button is clicked
            on_audio_input: Function to process audio input
        """
        super().__init__(on_generate_melody, on_end_practice, on_audio_input)
        self.config = config
        self._initialize_interval_settings()

    def _initialize_interval_settings(self):
        """Initialize interval settings from the configuration."""
        self.init_num_problems = self.config.interval_practice.num_problems
        interval = self.config.interval_practice.interval
        self.direction_options = ["Up", "Down"]
        self.initial_direction = "Up" if interval >= 0 else "Down"
        absolute_interval = abs(interval)
        self.initial_interval_key = next(
            (
                key
                for key, value in Intervals.INTERVALS_MAP.items()
                if value == absolute_interval
            ),
            "minor 2nd",  # Default value if no match is found
        )

    def _build_interface(self) -> gr.Blocks:
        """Create and configure the Gradio interface.

        Returns:
            gr.Blocks: The Gradio interface.
        """
        with gr.Blocks(
            head="""
            <script src="https://cdn.jsdelivr.net/npm/tone@14.8.39/build/Tone.js">
            </script>
        """
        ) as app:
            self._add_header()
            with gr.Row():
                self.interval_box = gr.Dropdown(
                    list(Intervals.INTERVALS_MAP.keys()),
                    label="Interval",
                    value=self.initial_interval_key,
                )
                self.direction_box = gr.Radio(
                    self.direction_options,
                    label="Direction",
                    value=self.initial_direction,
                )
                self.number_problems_box = gr.Number(
                    label="Number of Problems", value=self.init_num_problems
                )

            self.generate_melody_button = gr.Button("Generate Melody")
            self.base_note_box = gr.Textbox(
                label="Base Note", value="", elem_id="base-note-box", visible=False
            )
            with gr.Row():
                self.phrase_info_box = gr.Textbox(label="Problem Information", value="")
                self.pitch_result_box = gr.Textbox(label="Pitch Result", value="")
            self.results_table = gr.DataFrame(
                headers=[
                    "Problem Number",
                    "Base Note",
                    "Target Note",
                    "Detected Note",
                    "Result",
                ],
                datatype=["number", "str", "str", "str", "str"],
                value=[],
                label="Result History",
            )

            self._add_audio_input()
            self.end_practice_button = gr.Button("End Practice")

            self._add_buttons_callbacks()

            # Add Tone.js script
            app.load(
                fn=None,
                inputs=None,
                outputs=None,
                js="""
                () => {
                    const synth = new Tone.Synth().toDestination();
                    //synth.volume.value = 10;

                    let isPlaying = false;
                    let currentNote = null;

                    // check for #base-note-box
                    setInterval(() => {
                        const input = document.querySelector('#base-note-box textarea');
                        const note = input.value;

                        if (!note || note === '-' || note.trim() === '') {
                            if (isPlaying) {
                                synth.triggerRelease();
                                isPlaying = false;
                                currentNote = null;
                            }
                            return;
                        }

                        if (currentNote !== note) {
                            if (isPlaying) {
                                synth.triggerRelease();
                            }
                            currentNote = note;
                            synth.triggerAttack(currentNote.split('\\n')[0] + '3');
                            isPlaying = true;
                        }
                    }, 100);
                }
            """,
            )

        return app

    def _add_header(self):
        """Create the header section of the UI."""
        gr.Markdown("# Interval Practice\nSing the designated note!")

    def _add_buttons_callbacks(self):
        """Create the control buttons section."""
        # Connect button callbacks
        self.generate_melody_button.click(
            fn=self.on_generate_melody,
            inputs=[self.interval_box, self.direction_box, self.number_problems_box],
            outputs=[
                self.base_note_box,
                self.phrase_info_box,
                self.pitch_result_box,
                self.results_table,
            ],
        )

        self.end_practice_button.click(
            fn=self.on_end_practice,
            outputs=[self.base_note_box, self.phrase_info_box, self.pitch_result_box],
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
            outputs=[
                self.base_note_box,
                self.phrase_info_box,
                self.pitch_result_box,
                self.results_table,
            ],
            show_progress=False,
            stream_every=0.1,
        )
