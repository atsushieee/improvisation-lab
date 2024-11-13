"""Main module to demonstrate melody generation with chord progression."""

from time import sleep

from improvisation_lab.config import AudioConfig, ChordProgression
from improvisation_lab.domain.music_theory import Notes
from improvisation_lab.domain.audio_input import MicInput, PitchDetector
from improvisation_lab.domain.melody_jam import PhraseGenerator, MelodyComposer

class MelodyApp:
    def __init__(self):
        self.phrase_generator = PhraseGenerator()
        self.melody_composer = MelodyComposer(self.phrase_generator)
        self.pitch_detector = PitchDetector(sample_rate=AudioConfig.SAMPLE_RATE)
        self.mic_input = MicInput(
            sample_rate=AudioConfig.SAMPLE_RATE,
            buffer_duration=AudioConfig.BUFFER_DURATION
        )
        self.current_note = None

    def _process_audio(self, audio_data):
        frequency = self.pitch_detector.detect_pitch(audio_data)
        target_note = "---" if self.current_note is None else self.current_note
        if frequency > 0:  # voice detected
            note_name = Notes.convert_frequency_to_note(frequency)
            print(f"\rTarget: {target_note:<5} | Your note: {note_name:<10}", end="", flush=True)
        else:  # no voice detected
            print(f"\rTarget: {target_note:<5} | Your note: ---          ", end="", flush=True)

    def run(self):
        # Generate melody phrases
        phrases = self.melody_composer.generate_phrases(ChordProgression.FLY_ME_TO_THE_MOON)
        
        # Setup audio processing
        self.mic_input._callback = self._process_audio

        print("Generating melody for Fly Me to the Moon:")
        print("-" * 50)

        try:
            self.mic_input.start_recording()
            
            for i, phrase_data in enumerate(phrases, 1):
                print(f"\nPhrase {i} ({phrase_data.chord_name}, {phrase_data.scale_info}):")
                print(" -> ".join(phrase_data.notes))

                if i < len(phrases):
                    next_phrase = phrases[i]
                    print(f"Next: {next_phrase.chord_name} ({next_phrase.notes[0]})")
                
                print("\nSing this phrase! (3 seconds per note)")
                for note in phrase_data.notes:
                    self.current_note = note
                    sleep(AudioConfig.NOTE_DURATION)
                self.current_note = None
                print("\n" + "-" * 50)

        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            self.mic_input.stop_recording()

def main():
    app = MelodyApp()
    app.run()

if __name__ == "__main__":
    main()
