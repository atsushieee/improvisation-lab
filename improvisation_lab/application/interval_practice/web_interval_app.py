"""Web application for interval practice."""

from typing import Tuple

import numpy as np

from improvisation_lab.application.base_app import BasePracticeApp
from improvisation_lab.config import Config
from improvisation_lab.domain.music_theory import Intervals
from improvisation_lab.infrastructure.audio import WebAudioProcessor
from improvisation_lab.presentation.interval_practice import (
    IntervalViewTextManager, WebIntervalPracticeView)
from improvisation_lab.service import IntervalPracticeService


class WebIntervalPracticeApp(BasePracticeApp):
    """Web application class for interval practice."""

    def __init__(self, service: IntervalPracticeService, config: Config):
        """Initialize the application using web UI.

        Args:
            service: IntervalPracticeService instance.
            config: Config instance.
        """
        super().__init__(service, config)

        self.audio_processor = WebAudioProcessor(
            sample_rate=config.audio.sample_rate,
            callback=self._process_audio_callback,
            buffer_duration=config.audio.buffer_duration,
        )

        self.text_manager = IntervalViewTextManager()
        self.ui = WebIntervalPracticeView(
            on_generate_melody=self.start,
            on_end_practice=self.stop,
            on_audio_input=self.handle_audio,
            config=config,
        )
        self.base_note = "-"

    def _process_audio_callback(self, audio_data: np.ndarray):
        """Process incoming audio data and update the application state.

        Args:
            audio_data: Audio data to process.
        """
        if not self.is_running or not self.phrases:
            return

        current_note = self.phrases[self.current_phrase_idx][
            self.current_note_idx
        ].value

        result = self.service.process_audio(audio_data, current_note)

        # Update status display
        self.text_manager.update_pitch_result(result)

        # Progress to next note if current note is complete
        if result.remaining_time <= 0:
            self._advance_to_next_note()

        self.text_manager.update_phrase_text(self.current_phrase_idx, self.phrases)

    def _advance_to_next_note(self):
        """Advance to the next note or phrase."""
        if self.phrases is None:
            return
        self.current_note_idx += 1
        if self.current_note_idx >= len(self.phrases[self.current_phrase_idx]):
            self.current_note_idx = 0
            self.current_phrase_idx += 1
            if self.current_phrase_idx >= len(self.phrases):
                self.current_phrase_idx = 0
            self.base_note = self.phrases[self.current_phrase_idx][
                self.current_note_idx
            ].value

    def handle_audio(self, audio: Tuple[int, np.ndarray]) -> Tuple[str, str, str]:
        """Handle audio input from Gradio interface.

        Args:
            audio: Audio data to process.

        Returns:
            Tuple[str, str, str]:
                The current base note including the next base note,
                target note, and result text.
        """
        if not self.is_running:
            return "-", "Not running", "Start the session first"

        self.audio_processor.process_audio(audio)
        return (
            self.base_note,
            self.text_manager.phrase_text,
            self.text_manager.result_text,
        )

    def start(
        self, interval: str, direction: str, number_problems: int
    ) -> Tuple[str, str, str]:
        """Start a new practice session.

        Args:
            interval: Interval to move to and back.
            direction: Direction to move to and back.
            number_problems: Number of problems to generate.

        Returns:
            Tuple[str, str, str]:
                The current base note including the next base note,
                target note, and result text.
        """
        semitone_interval = Intervals.INTERVALS_MAP.get(interval, 0)

        if direction == "Down":
            semitone_interval = -semitone_interval
        self.phrases = self.service.generate_melody(
            num_notes=number_problems, interval=semitone_interval
        )
        self.current_phrase_idx = 0
        self.current_note_idx = 0
        self.is_running = True

        present_note = self.phrases[0][0].value
        self.base_note = present_note

        if not self.audio_processor.is_recording:
            self.text_manager.initialize_text()
            self.audio_processor.start_recording()

        self.text_manager.update_phrase_text(self.current_phrase_idx, self.phrases)

        return (
            self.base_note,
            self.text_manager.phrase_text,
            self.text_manager.result_text,
        )

    def stop(self) -> Tuple[str, str, str]:
        """Stop the current practice session.

        Returns:
            tuple[str, str, str]:
                The current base note including the next base note,
                target note, and result text.
        """
        self.is_running = False
        self.base_note = "-"
        if self.audio_processor.is_recording:
            self.audio_processor.stop_recording()
            self.text_manager.terminate_text()
        return (
            self.base_note,
            self.text_manager.phrase_text,
            self.text_manager.result_text,
        )

    def launch(self, **kwargs):
        """Launch the application."""
        self.ui.launch(**kwargs)
