"""Console application for melody practice."""

import time

import numpy as np

from improvisation_lab.application.melody_practice.base_app import \
    BaseMelodyPracticeApp
from improvisation_lab.config import Config
from improvisation_lab.infrastructure.audio import DirectAudioProcessor
from improvisation_lab.presentation.melody_practice import ConsoleMelodyView
from improvisation_lab.service import MelodyPracticeService


class ConsoleMelodyPracticeApp(BaseMelodyPracticeApp):
    """Main application class for melody practice."""

    def __init__(self, service: MelodyPracticeService, config: Config):
        """Initialize the application using console UI.

        Args:
            service: MelodyPracticeService instance.
            config: Config instance.
        """
        super().__init__(service, config)

        self.audio_processor = DirectAudioProcessor(
            sample_rate=config.audio.sample_rate,
            callback=self._process_audio_callback,
            buffer_duration=config.audio.buffer_duration,
        )

        self.ui = ConsoleMelodyView(self.text_manager, config.selected_song)

    def _process_audio_callback(self, audio_data: np.ndarray):
        """Process incoming audio data and update the application state.

        Args:
            audio_data: Audio data to process.
        """
        if self.phrases is None:
            return
        current_phrase = self.phrases[self.current_phrase_idx]
        current_note = current_phrase.notes[self.current_note_idx]

        result = self.service.process_audio(audio_data, current_note)
        self.ui.display_pitch_result(result)

        # Progress to next note if current note is complete
        if result.remaining_time <= 0:
            self._advance_to_next_note()

    def _advance_to_next_note(self):
        """Advance to the next note or phrase."""
        if self.phrases is None:
            return
        self.current_note_idx += 1
        if self.current_note_idx >= len(self.phrases[self.current_phrase_idx].notes):
            self.current_note_idx = 0
            self.current_phrase_idx += 1
            self.ui.display_phrase_info(self.current_phrase_idx, self.phrases)
            if self.current_phrase_idx >= len(self.phrases):
                self.current_phrase_idx = 0

    def launch(self):
        """Launch the application."""
        self.ui.launch()
        self.phrases = self.service.generate_melody()
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
