"""Tests for IntervalPracticeService."""

from improvisation_lab.config import Config
from improvisation_lab.domain.music_theory import Notes
from improvisation_lab.service.interval_practice_service import \
    IntervalPracticeService


class TestPiecePracticeService:

    def test_generate_melody(self):
        """Test melody generation."""
        config = Config()
        service = IntervalPracticeService(config)
        melody = service.generate_melody(num_notes=10, interval=2)
        # 10 notes, each with 2 parts (base, transposed)
        assert len(melody) == 10
        assert all(len(note_group) == 2 for note_group in melody)
        assert all(
            isinstance(note, Notes) for note_group in melody for note in note_group
        )
