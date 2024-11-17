"""Script for demonstrating pitch detection functionality."""

import time

from improvisation_lab.config import Config
from improvisation_lab.domain.analysis import PitchDetector
from improvisation_lab.domain.music_theory import Notes
from improvisation_lab.infrastructure.audio import MicInput

def main(config: Config):
    """Run pitch detection demo.
    
    Args:
        config: Configuration object.
    """
    pitch_detector = PitchDetector(config.audio.pitch_detector)
    mic_input = MicInput(
        sample_rate=config.audio.sample_rate,
        buffer_duration=config.audio.buffer_duration,
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
    config = Config()
    main(config)
