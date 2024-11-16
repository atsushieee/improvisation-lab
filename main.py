"""Main module to demonstrate melody generation with chord progression."""

import time

import numpy as np

from improvisation_lab.config import Config
from improvisation_lab.domain.audio_input import MicInput, PitchDetector
from improvisation_lab.domain.melody_jam import (MelodyComposer, PhraseData,
                                                 PhraseGenerator)
from improvisation_lab.domain.music_theory import Notes


class MelodyApp:
    """Application class for melody generation and real-time pitch detection.

    This class combines melody generation with real-time pitch detection,
    allowing users to practice singing generated melodies while receiving
    immediate feedback on their pitch accuracy.
    """

    def __init__(self, config: Config):
        """Initialize MelodyApp with configuration.

        Args:
            config:
                Configuration object containing audio settings and chord progressions.
        """
        self.phrase_generator = PhraseGenerator()
        self.melody_composer = MelodyComposer(self.phrase_generator)
        self.config = config
        self.pitch_detector = PitchDetector(self.config.audio.pitch_detector)
        self.mic_input = MicInput(
            sample_rate=self.config.audio.sample_rate,
            buffer_duration=self.config.audio.buffer_duration,
        )
        self.current_note: str | None = None
        self.correct_pitch_start_time: float | None = None
        self.note_completed = False

    def _process_audio(self, audio_data: np.ndarray):
        """Process audio data to detect pitch and provide feedback.

        Args:
            audio_data: Audio data as a numpy array.
        """
        frequency = self.pitch_detector.detect_pitch(audio_data)
        target_note = "---" if self.current_note is None else self.current_note

        if frequency <= 0:  # if no voice detected, reset the correct pitch start time
            self.correct_pitch_start_time = None
            self._display_no_voice(target_note)
            return

        note_name = Notes.convert_frequency_to_base_note(frequency)
        # if the detected note is different, reset the correct pitch start time
        if note_name != self.current_note:
            self.correct_pitch_start_time = None
            self._display_incorrect_pitch(target_note, note_name)
            return

        current_time = time.time()
        # Note is completed if the correct pitch is sustained for the duration of a note
        if self.correct_pitch_start_time is None:
            self.correct_pitch_start_time = current_time
            remaining = self.config.audio.note_duration
        else:
            elapsed = current_time - self.correct_pitch_start_time
            if elapsed >= self.config.audio.note_duration:
                self.note_completed = True
            remaining = max(0, self.config.audio.note_duration - elapsed)

        self._display_correct_pitch(target_note, note_name, remaining)

    def _display_no_voice(self, target_note: str):
        """Display feedback when no voice is detected.

        Args:
            target_note: The target note to display.
        """
        message = (
            f"\rTarget: {target_note:<5} | "
            f"Your note: ---                                          "
        )
        print(message, end="", flush=True)

    def _display_incorrect_pitch(self, target_note: str, note_name: str):
        """Display feedback when incorrect pitch is detected.

        Args:
            target_note: The target note to display.
            note_name: The detected note to display.
        """
        message = (
            f"\rTarget: {target_note:<5} | "
            f"Your note: {note_name:<10}                              "
        )
        print(message, end="", flush=True)

    def _display_correct_pitch(
        self, target_note: str, note_name: str, remaining: float
    ):
        """Display feedback when correct pitch is detected.

        Args:
            target_note: The target note to display.
            note_name: The detected note to display.
            remaining: The remaining time to display.
        """
        message = (
            f"\rTarget: {target_note:<5} | "
            f"Your note: {note_name:<10} | "
            f"Remaining: {remaining:.1f}s"
        )
        print(message, end="", flush=True)

    def _process_phrases(self, phrases: list[PhraseData]):
        """Process a single phrase of the melody.

        Args:
            phrases: List of phrases to process.
        """
        for i, phrase_data in enumerate(phrases, 1):
            print(f"\nPhrase{i} ({phrase_data.chord_name}, {phrase_data.scale_info}):")
            print(" -> ".join(phrase_data.notes))

            if i < len(phrases):
                next_phrase = phrases[i]
                print(f"Next: {next_phrase.chord_name} ({next_phrase.notes[0]})")

            print("\nSing each note for 1 second!")
            self._process_notes(phrase_data.notes)
            print("\n" + "-" * 50)

    def _process_notes(self, notes: list[str]):
        """Process each note in a phrase.

        Args:
            notes: List of notes to process.
        """
        for note in notes:
            self.current_note = note
            self.note_completed = False
            self.correct_pitch_start_time = None

            while not self.note_completed:
                time.sleep(0.1)
        self.current_note = None

    def run(self):
        """Run the melody generation and practice session.

        Generates melody phrases based on the configured chord progression and
        starts a practice session where users can sing along while receiving
        real-time pitch feedback.
        """
        # Generate melody phrases using the selected song
        selected_progression = self.config.chord_progressions[self.config.selected_song]
        phrases = self.melody_composer.generate_phrases(selected_progression)

        # Setup audio processing
        self.mic_input._callback = self._process_audio

        print(f"Generating melody for {self.config.selected_song}:")
        print("-" * 50)

        try:
            self.mic_input.start_recording()
            self._process_phrases(phrases)

        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            self.mic_input.stop_recording()


def main():
    """Entry point for the melody generation application.

    Creates and runs an instance of MelodyApp with the default configuration.
    """
    config = Config()
    app = MelodyApp(config)
    app.run()


if __name__ == "__main__":
    main()
