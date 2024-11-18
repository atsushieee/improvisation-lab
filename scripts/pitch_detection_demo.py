"""Script for demonstrating pitch detection functionality."""

import argparse
import time

import gradio as gr

from improvisation_lab.config import Config
from improvisation_lab.domain.analysis import PitchDetector
from improvisation_lab.domain.music_theory import Notes
from improvisation_lab.infrastructure.audio import GradioAudioInput, MicInput


def create_process_audio(pitch_detector: PitchDetector):
    """Create audio processing callback function.

    Args:
        pitch_detector: PitchDetector instance

    Returns:
        Callback function for processing audio data
    """
    def process_audio(audio_data):
        frequency = pitch_detector.detect_pitch(audio_data)
        if frequency > 0:  # voice detected
            note_name = Notes.convert_frequency_to_note(frequency)
            print(
                f"\rFrequency: {frequency:6.1f} Hz | Note: {note_name:<5}", end="",
                flush=True
            )
        else:  # no voice detected
            print("\rNo voice detected                        ", end="", flush=True)
    return process_audio


def run_mic_demo(config: Config):
    """Run pitch detection demo using microphone input.

    Args:
        config: Configuration object
    """
    pitch_detector = PitchDetector(config.audio.pitch_detector)
    mic_input = MicInput(
        sample_rate=config.audio.sample_rate,
        buffer_duration=config.audio.buffer_duration,
    )

    print("Starting pitch detection demo (Microphone)...")
    print("Sing or hum a note!")
    print("-" * 50)

    try:
        mic_input._callback = create_process_audio(pitch_detector)
        mic_input.start_recording()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        mic_input.stop_recording()


def run_gradio_demo(config: Config):
    """Run pitch detection demo using Gradio interface.

    Args:
        config: Configuration object
    """
    pitch_detector = PitchDetector(config.audio.pitch_detector)
    audio_input = GradioAudioInput(
        sample_rate=config.audio.sample_rate,
        buffer_duration=config.audio.buffer_duration,
    )

    print("Starting pitch detection demo (Gradio)...")
    result = {"text": "No voice detected"}

    def process_audio(audio_data):
        frequency = pitch_detector.detect_pitch(audio_data)
        if frequency > 0:
            note_name = Notes.convert_frequency_to_note(frequency)
            result["text"] = f"Frequency: {frequency:6.1f} Hz | Note: {note_name}"
        else:
            result["text"] = "No voice detected"

    audio_input._callback = process_audio

    def handle_audio(audio):
        """Handle audio input from Gradio."""
        if audio is None:
            return result["text"]
        if not audio_input.is_recording:
            audio_input.start_recording()
        audio_input.process_audio(audio)
        return result["text"]

    interface = gr.Interface(
        fn=handle_audio,
        inputs=gr.Audio(
            sources=["microphone"],
            streaming=True,
            type="numpy",
        ),
        outputs=gr.Text(label="Detection Result"),
        live=True,
        title="Pitch Detection Demo",
        allow_flagging="never",
        stream_every=0.05,
    )
    interface.queue()
    interface.launch(
        share=False,
        debug=True,
    )


def main():
    """Run the pitch detection demo."""
    parser = argparse.ArgumentParser(description="Run pitch detection demo")
    parser.add_argument(
        "--input",
        choices=["mic", "gradio"],
        default="mic",
        help="Input method (mic or gradio)",
    )
    args = parser.parse_args()

    config = Config()

    if args.input == "mic":
        run_mic_demo(config)
    else:
        run_gradio_demo(config)


if __name__ == "__main__":
    main()
