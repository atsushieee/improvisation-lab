"""Tests for BasePracticeService."""

import time

import numpy as np
import pytest

from improvisation_lab.config import Config
from improvisation_lab.service.base_practice_service import PitchResult
from improvisation_lab.service.piece_practice_service import \
    BasePracticeService


class MockBasePracticeService(BasePracticeService):
    def generate_melody(self):
        pass


class TestBasePracticeService:
    @pytest.fixture
    def init_module(self):
        """Create BasePracticeService instance for testing."""
        config = Config()
        self.service = MockBasePracticeService(config)

    @pytest.mark.usefixtures("init_module")
    def test_process_audio_no_voice(self):
        """Test processing audio with no voice detected."""
        audio_data = np.zeros(1024, dtype=np.float32)
        result = self.service.process_audio(audio_data, target_note="A")

        assert isinstance(result, PitchResult)
        assert result.current_base_note is None
        assert not result.is_correct

    @pytest.mark.usefixtures("init_module")
    def test_process_audio_with_voice(self):
        """Test processing audio with voice detected."""
        sample_rate = 16000
        duration = 0.1
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * 440 * t)

        result = self.service.process_audio(audio_data, target_note="A")

        assert isinstance(result, PitchResult)
        assert result.current_base_note == "A"
        assert result.is_correct

    @pytest.mark.usefixtures("init_module")
    def test_process_audio_incorrect_pitch(self):
        """Test processing audio with incorrect pitch."""
        sample_rate = 16000
        duration = 0.1
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Generate 440Hz (A4) when target is C4
        audio_data = np.sin(2 * np.pi * 440 * t)

        result = self.service.process_audio(audio_data, target_note="C")

        assert isinstance(result, PitchResult)
        assert result.current_base_note == "A"
        assert not result.is_correct
        assert result.remaining_time == self.service.config.audio.note_duration

    @pytest.mark.usefixtures("init_module")
    def test_correct_pitch_timing(self):
        """Test timing behavior with correct pitch."""
        sample_rate = 16000
        duration = 0.1
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * 440 * t)

        # First detection
        result1 = self.service.process_audio(audio_data, target_note="A")
        initial_time = self.service.correct_pitch_start_time
        assert result1.is_correct
        assert result1.remaining_time == self.service.config.audio.note_duration

        # Wait a bit
        time.sleep(0.5)

        # Second detection
        result2 = self.service.process_audio(audio_data, target_note="A")
        assert result2.is_correct
        assert result2.remaining_time < self.service.config.audio.note_duration
        assert initial_time == self.service.correct_pitch_start_time

    @pytest.mark.usefixtures("init_module")
    def test_correct_pitch_completion(self):
        """Test completion of correct pitch duration."""
        sample_rate = 16000
        duration = 0.1
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * 440 * t)

        # First detection
        result1 = self.service.process_audio(audio_data, target_note="A")
        assert result1.remaining_time == self.service.config.audio.note_duration

        # Wait for full duration
        time.sleep(self.service.config.audio.note_duration + 0.1)

        # Final detection
        result2 = self.service.process_audio(audio_data, target_note="A")
        assert result2.remaining_time == 0
