"""Module for web-based melody visualization."""

import gradio as gr

from improvisation_lab.presentation.melody_view import MelodyView, NoteDisplay


class WebInterfaceView(MelodyView):
    """Web-based implementation of melody visualization."""

    def __init__(self, gradio_module: gr):
        """Initialize web interface view.

        Args:
            gradio_module:
                Gradio module for web interface creation.
                Can be replaced with a mock object during testing
                to avoid actual GUI creation and network operations.
        """
        self.gr = gradio_module
        self.phrase_info = ""
        self.current_phrase_info = ""
        self.next_phrase_info = ""
        self.note_status = ""
        self.interface = None
        self._outputs: dict[str, gr.components.Component] = {}

    def _create_interface(self, song_name: str) -> gr.Blocks:
        """Create Gradio interface components.

        Args:
            song_name: The name of the song to be displayed in the title.

        Returns:
            Gradio interface.
        """
        with self.gr.Blocks(title=f"Melody Practice: {song_name}") as interface:
            with self.gr.Row():
                self.gr.Markdown("Sing each note for 1 second!")
            with self.gr.Row():
                self._outputs["phrase"] = self.gr.Textbox(
                    label="Phrase Information",
                    value=self.phrase_info,
                    interactive=False,
                )
            with self.gr.Row():
                self._outputs["note"] = self.gr.Textbox(
                    label="Note Status",
                    value=self.note_status,
                    interactive=False,
                )
                self.audio_input = self.gr.Audio(
                    sources=["microphone"],
                    streaming=True,
                    type="numpy",
                )
        return interface

    def run(self, song_name: str, share: bool = False, debug: bool = False):
        """Run the web interface.

        Args:
            song_name: Name of the song to be practiced.
            share: Whether to create a public link. Defaults to False.
            debug: Whether to run the interface in debug mode. Defaults to False.
        """
        self.interface = self._create_interface(song_name)
        if self.interface is not None:
            self.interface.queue()
            self.interface.launch(share=share, debug=debug)

    def _update_phrase_display(self):
        self.phrase_info = self.current_phrase_info + "\n" + self.next_phrase_info
        if self.interface is not None:
            self._outputs["phrase"].update(value=self.phrase_info)

    def display_phrase_info(
        self,
        phrase_number: int,
        chord_name: str,
        scale_info: str,
        notes: list[str],
        display_is_updated: bool = False,
    ):
        """Display information about the current phrase.

        Args:
            phrase_number: The current phrase number
            chord_name: Name of the chord
            scale_info: Scale information
            notes: List of notes in the phrase
            display_is_updated: Whether to update the display. Defaults to False.
        """
        self.current_phrase_info = (
            f"Phrase{phrase_number} ({chord_name}, {scale_info}):\n"
            + " -> ".join(notes)
        )
        if display_is_updated:
            self._update_phrase_display()

    def display_next_phrase_info(
        self, chord_name: str, first_note: str, display_is_updated: bool = True
    ):
        """Display information about the next phrase.

        Args:
            chord_name: Name of the next chord
            first_note: First note of the next phrase
            display_is_updated: Whether to update the display. Defaults to True.
        """
        self.next_phrase_info = f"Next: {chord_name} ({first_note})"
        if display_is_updated:
            self._update_phrase_display()

    def display_note_status(self, note_info: NoteDisplay):
        """Display current note status.

        Args:
            note_info: Information about the current note status
        """
        if note_info.current_note is None:
            note_status = f"Target: {note_info.target_note:<5} | Your note: ---"
        elif note_info.remaining_time is None:
            note_status = (
                f"Target: {note_info.target_note:<5} | "
                f"Your note: {note_info.current_note:<10}"
            )
        else:
            note_status = (
                f"Target: {note_info.target_note:<5} | "
                f"Your note: {note_info.current_note:<10} | "
                f"Remaining: {note_info.remaining_time:.1f}s"
            )
        self.note_status = note_status
        if self.interface is not None:
            self._outputs["note"].update(value=self.note_status)

    def display_practice_end(self):
        """Display practice session end message."""
        end_message = "Stopping..."
        self.phrase_info = end_message
        if self.interface is not None:
            self._outputs["phrase"].update(value=self.phrase_info)
