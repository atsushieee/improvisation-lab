"""Web application for melody practice."""

from typing import Tuple

import numpy as np

from improvisation_lab.application.base_app import BasePracticeApp
from improvisation_lab.config import Config
from improvisation_lab.infrastructure.audio import WebAudioProcessor
from improvisation_lab.presentation.piece_practice import (
    PieceViewTextManager, WebPiecePracticeView)
from improvisation_lab.service import PiecePracticeService


class WebPiecePracticeApp(BasePracticeApp):
    """Web application class for piece practice."""

    def __init__(self, service: PiecePracticeService, config: Config):
        """Initialize the application using web UI.

        Args:
            service: PiecePracticeService instance.
            config: Config instance.
        """
        super().__init__(service, config)

        self.audio_processor = WebAudioProcessor(
            sample_rate=config.audio.sample_rate,
            callback=self._process_audio_callback,
            buffer_duration=config.audio.buffer_duration,
        )

        self.text_manager = PieceViewTextManager()
        self.ui = WebPiecePracticeView(
            on_generate_melody=self.start,
            on_end_practice=self.stop,
            on_audio_input=self.handle_audio,
            song_name=config.piece_practice.selected_song,
        )

    def _process_audio_callback(self, audio_data: np.ndarray):
        """Process incoming audio data and update the application state.

        Args:
            audio_data: Audio data to process.
        """
        if not self.is_running or not self.phrases:
            return

        current_phrase = self.phrases[self.current_phrase_idx]
        current_note = current_phrase.notes[self.current_note_idx]

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
        if self.current_note_idx >= len(self.phrases[self.current_phrase_idx].notes):
            self.current_note_idx = 0
            self.current_phrase_idx += 1
            if self.current_phrase_idx >= len(self.phrases):
                self.current_phrase_idx = 0

    def handle_audio(self, audio: Tuple[int, np.ndarray]) -> Tuple[str, str]:
        """Handle audio input from Gradio interface.

        Args:
            audio: Audio data to process.

        Returns:
            tuple[str, str]: The current phrase text and result text.
        """
        if not self.is_running:
            return "Not running", "Start the session first"

        self.audio_processor.process_audio(audio)
        return self.text_manager.phrase_text, self.text_manager.result_text

    def start(self) -> tuple[str, str]:
        """Start a new practice session.

        Returns:
            tuple[str, str]: The current phrase text and result text.
        """
        self.phrases = self.service.generate_melody()
        self.current_phrase_idx = 0
        self.current_note_idx = 0
        self.is_running = True

        if not self.audio_processor.is_recording:
            self.text_manager.initialize_text()
            self.audio_processor.start_recording()

        self.text_manager.update_phrase_text(self.current_phrase_idx, self.phrases)
        return self.text_manager.phrase_text, self.text_manager.result_text

    def stop(self) -> tuple[str, str]:
        """Stop the current practice session.

        Returns:
            tuple[str, str]: The current phrase text and result text.
        """
        self.is_running = False
        if self.audio_processor.is_recording:
            self.audio_processor.stop_recording()
            self.text_manager.terminate_text()
        return self.text_manager.phrase_text, self.text_manager.result_text

    def launch(self, **kwargs):
        """Launch the application."""
        self.ui.launch(**kwargs)
