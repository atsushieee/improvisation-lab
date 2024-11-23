"""Module for console-based melody visualization."""

from improvisation_lab.presentation.melody_view import MelodyView, NoteDisplay


class ConsoleView(MelodyView):
    """Console-based implementation of melody visualization."""

    def display_practice_start(self, song_name: str):
        """Display practice start message in console.

        Args:
            song_name: Name of the song to be practiced.
        """
        print(f"Generating melody for {song_name}:")
        print("-" * 50)

    def display_phrase_info(
        self, phrase_number: int, chord_name: str, scale_info: str, notes: list[str]
    ):
        """Display phrase information in console.

        Args:
            phrase_number: Number of the phrase.
            chord_name: Name of the chord.
            scale_info: Information about the scale.
            notes: List of notes in the phrase.
        """
        print(f"\nPhrase{phrase_number} ({chord_name}, {scale_info}):")
        print(" -> ".join(notes))

    def display_next_phrase_info(self, chord_name: str, first_note: str):
        """Display next phrase information in console.

        Args:
            chord_name: Name of the chord.
            first_note: First note of the next phrase.
        """
        print(f"Next: {chord_name} ({first_note})")

    def display_singing_instruction(self):
        """Display singing instruction for the user."""
        print("Sing each note for 1 second!")

    def display_note_status(self, note_info: NoteDisplay):
        """Display note status in console.

        Args:
            note_info: Information about the note.
        """
        if note_info.current_note is None:
            message = (
                f"\rTarget: {note_info.target_note:<5} | "
                f"Your note: ---                                          "
            )
        elif note_info.remaining_time is None:
            message = (
                f"\rTarget: {note_info.target_note:<5} | "
                f"Your note: {note_info.current_note:<10}                              "
            )
        else:
            message = (
                f"\rTarget: {note_info.target_note:<5} | "
                f"Your note: {note_info.current_note:<10} | "
                f"Remaining: {note_info.remaining_time:.1f}s"
            )
        print(message, end="", flush=True)

    def display_practice_end(self):
        """Display practice end message in console."""
        print("\nStopping...")
