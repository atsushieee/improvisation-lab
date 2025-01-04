"""Console application for all practices."""

import time
from abc import ABC, abstractmethod
from typing import Optional

import numpy as np

from improvisation_lab.application.base_app import BasePracticeApp
from improvisation_lab.config import Config
from improvisation_lab.infrastructure.audio import DirectAudioProcessor
from improvisation_lab.presentation.console_view import ConsolePracticeView
from improvisation_lab.service.base_practice_service import BasePracticeService


class ConsoleBasePracticeApp(BasePracticeApp, ABC):
    """Console application class for all practices."""

    def __init__(self, service: BasePracticeService, config: Config):
        """Initialize the application using console UI.

        Args:
            service: PracticeService instance.
            config: Config instance.
        """
        super().__init__(service, config)

        self.audio_processor = DirectAudioProcessor(
            sample_rate=config.audio.sample_rate,
            callback=self._process_audio_callback,
            buffer_duration=config.audio.buffer_duration,
        )
        self.ui: Optional[ConsolePracticeView] = None

    def _process_audio_callback(self, audio_data: np.ndarray):
        """Process incoming audio data and update the application state.

        Args:
            audio_data: Audio data to process.
        """
        if self.phrases is None:
            return
        current_note = self._get_current_note()

        result = self.service.process_audio(audio_data, current_note)
        if self.ui is not None:
            self.ui.display_pitch_result(result)

        # Progress to next note if current note is complete
        if result.remaining_time <= 0:
            self._advance_to_next_note()

    def _advance_to_next_note(self):
        """Advance to the next note or phrase."""
        if self.phrases is None:
            return
        self.current_note_idx += 1
        if self.current_note_idx >= len(self._get_current_phrase()):
            self.current_note_idx = 0
            self.current_phrase_idx += 1
            if self.current_phrase_idx >= len(self.phrases):
                self.current_phrase_idx = 0
            self.ui.display_phrase_info(self.current_phrase_idx, self.phrases)

    def launch(self):
        """Launch the application."""
        self.ui.launch()
        self.phrases = self._generate_melody()
        self.current_phrase_idx = 0
        self.current_note_idx = 0
        self.is_running = True

        if not self.audio_processor.is_recording:
            try:
                self.audio_processor.start_recording()
                self.ui.display_phrase_info(self.current_phrase_idx, self.phrases)
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("\nStopping...")
            finally:
                self.audio_processor.stop_recording()

    @abstractmethod
    def _get_current_note(self):
        """Return the current note to be processed."""
        pass

    @abstractmethod
    def _get_current_phrase(self):
        """Return the current phrase to be processed."""
        pass

    @abstractmethod
    def _generate_melody(self):
        """Generate melody specific to the practice type."""
        pass
