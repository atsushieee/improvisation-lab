"""Main module to demonstrate melody generation with chord progression."""

from time import sleep

import numpy as np

from improvisation_lab.config import Config
from improvisation_lab.domain.audio_input import MicInput, PitchDetector
from improvisation_lab.domain.melody_jam import MelodyComposer, PhraseGenerator
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
        self.current_note = None

    def _process_audio(self, audio_data: np.ndarray):
        """Process audio data to detect pitch and provide feedback.

        Args:
            audio_data: Audio data as a numpy array.
        """
        frequency = self.pitch_detector.detect_pitch(audio_data)
        target_note = "---" if self.current_note is None else self.current_note
        if frequency > 0:  # voice detected
            note_name = Notes.convert_frequency_to_note(frequency)
            print(
                f"\rTarget: {target_note:<5} | Your note: {note_name:<10}",
                end="",
                flush=True,
            )
        else:  # no voice detected
            print(
                f"\rTarget: {target_note:<5} | Your note: ---          ",
                end="",
                flush=True,
            )

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

            for i, phrase_data in enumerate(phrases, 1):
                print(
                    f"\nPhrase{i} ({phrase_data.chord_name}, {phrase_data.scale_info}):"
                )
                print(" -> ".join(phrase_data.notes))

                if i < len(phrases):
                    next_phrase = phrases[i]
                    print(f"Next: {next_phrase.chord_name} ({next_phrase.notes[0]})")

                print("\nSing this phrase! (3 seconds per note)")
                for note in phrase_data.notes:
                    self.current_note = note
                    sleep(self.config.audio.note_duration)
                self.current_note = None
                print("\n" + "-" * 50)

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
