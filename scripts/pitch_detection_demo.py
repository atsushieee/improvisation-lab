"""Script for demonstrating pitch detection functionality."""

import time

from improvisation_lab.config import AudioConfig
from improvisation_lab.domain.audio_input import MicInput, PitchDetector
from improvisation_lab.domain.music_theory import Notes


def main():
    """Run pitch detection demo."""
    pitch_detector = PitchDetector(sample_rate=AudioConfig.SAMPLE_RATE)
    mic_input = MicInput(
        sample_rate=AudioConfig.SAMPLE_RATE,
        buffer_duration=AudioConfig.BUFFER_DURATION
    )

    def process_audio(audio_data):
        frequency = pitch_detector.detect_pitch(audio_data)
        if frequency > 0:  # voice detected
            note_name = Notes.convert_frequency_to_note(frequency)
            print(f"\rFrequency: {frequency:6.1f} Hz | Note: {note_name:<5}", end="", flush=True)
        else:  # no voice detected
            print(f"\rNo voice detected                        ", end="", flush=True)

    print("Starting pitch detection demo...")
    print("Sing or hum a note!")
    print("-" * 50)

    try:
        mic_input._callback = process_audio
        mic_input.start_recording()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        mic_input.stop_recording()


if __name__ == "__main__":
    main()
