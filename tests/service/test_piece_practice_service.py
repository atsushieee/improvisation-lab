"""Tests for PiecePracticeService."""

from improvisation_lab.config import Config
from improvisation_lab.service.piece_practice_service import \
    PiecePracticeService


class TestPiecePracticeService:

    def test_generate_melody(self):
        """Test melody generation."""
        config = Config()
        service = PiecePracticeService(config)
        phrases = service.generate_melody()
        assert len(phrases) > 0
        assert all(hasattr(phrase, "notes") for phrase in phrases)
        assert all(hasattr(phrase, "chord_name") for phrase in phrases)
        assert all(hasattr(phrase, "scale_info") for phrase in phrases)
        assert all(hasattr(phrase, "length") for phrase in phrases)
