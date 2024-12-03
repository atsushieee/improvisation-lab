"""Service for practicing melodies."""

import time
from dataclasses import dataclass

import numpy as np

from improvisation_lab.config import Config
from improvisation_lab.domain.analysis import PitchDetector
from improvisation_lab.domain.composition import MelodyComposer, PhraseData
from improvisation_lab.domain.music_theory import Notes


@dataclass
class PitchResult:
    """Result of pitch detection."""

    target_note: str
    current_base_note: str | None
    is_correct: bool
    remaining_time: float


class MelodyPracticeService:
    """Service for generating and processing melodies."""

    def __init__(self, config: Config):
        """Initialize MelodyPracticeService with configuration."""
        self.config = config
        self.melody_composer = MelodyComposer()
        self.pitch_detector = PitchDetector(config.audio.pitch_detector)

        self.correct_pitch_start_time: float | None = None

    def generate_melody(self) -> list[PhraseData]:
        """Generate a melody based on the configured chord progression.

        Returns:
            List of PhraseData instances representing the generated melody.
        """
        selected_progression = self.config.chord_progressions[self.config.selected_song]
        return self.melody_composer.generate_phrases(selected_progression)

    def process_audio(self, audio_data: np.ndarray, target_note: str) -> PitchResult:
        """Process audio data to detect pitch and provide feedback.

        Args:
            audio_data: Audio data as a numpy array.
            target_note: The target note to display.
        Returns:
            PitchResult containing the target note, detected note, correctness,
            and remaining time.
        """
        frequency = self.pitch_detector.detect_pitch(audio_data)

        if frequency <= 0:  # if no voice detected, reset the correct pitch start time
            return self._create_no_voice_result(target_note)

        note_name = Notes.convert_frequency_to_base_note(frequency)
        if note_name != target_note:
            return self._create_incorrect_pitch_result(target_note, note_name)

        return self._create_correct_pitch_result(target_note, note_name)

    def _create_no_voice_result(self, target_note: str) -> PitchResult:
        """Create result for no voice detected case.

        Args:
            target_note: The target note to display.

        Returns:
            PitchResult for no voice detected case.
        """
        self.correct_pitch_start_time = None
        return PitchResult(
            target_note=target_note,
            current_base_note=None,
            is_correct=False,
            remaining_time=self.config.audio.note_duration,
        )

    def _create_incorrect_pitch_result(
        self, target_note: str, detected_note: str
    ) -> PitchResult:
        """Create result for incorrect pitch case, reset the correct pitch start time.

        Args:
            target_note: The target note to display.
            detected_note: The detected note.

        Returns:
            PitchResult for incorrect pitch case.
        """
        self.correct_pitch_start_time = None
        return PitchResult(
            target_note=target_note,
            current_base_note=detected_note,
            is_correct=False,
            remaining_time=self.config.audio.note_duration,
        )

    def _create_correct_pitch_result(
        self, target_note: str, detected_note: str
    ) -> PitchResult:
        """Create result for correct pitch case.

        Args:
            target_note: The target note to display.
            detected_note: The detected note.

        Returns:
            PitchResult for correct pitch case.
        """
        current_time = time.time()
        # Note is completed if the correct pitch is sustained for the duration of a note
        if self.correct_pitch_start_time is None:
            self.correct_pitch_start_time = current_time
            remaining_time = self.config.audio.note_duration
        else:
            elapsed_time = current_time - self.correct_pitch_start_time
            remaining_time = max(0, self.config.audio.note_duration - elapsed_time)

        return PitchResult(
            target_note=target_note,
            current_base_note=detected_note,
            is_correct=True,
            remaining_time=remaining_time,
        )
