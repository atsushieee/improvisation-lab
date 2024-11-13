"""Tests for melody player module."""

import pytest

from improvisation_lab.domain.melody_jam import MelodyGenerator, MelodyPlayer


class TestMelodyPlayer:
    @pytest.fixture
    def init_module(self):
        """Initialize test module."""
        self.melody_generator = MelodyGenerator()
        self.melody_player = MelodyPlayer(self.melody_generator)

    @pytest.mark.usefixtures("init_module")
    def test_generate_phrases_basic(self):
        """Test basic phrase generation functionality."""
        progression = [
            ("C", "major", "C", "maj7", 4),
            ("A", "natural_minor", "A", "min7", 4),
        ]

        phrases = self.melody_player.generate_phrases(progression)

        # Test number of phrases
        assert len(phrases) == 2

        # Test first phrase structure
        first_phrase = phrases[0]
        assert len(first_phrase.notes) == 4
        assert first_phrase.chord_name == "Cmaj7"
        assert first_phrase.scale_info == "C major"
        assert first_phrase.length == 4

        # Test second phrase structure
        second_phrase = phrases[1]
        assert len(second_phrase.notes) == 4
        assert second_phrase.chord_name == "Amin7"
        assert second_phrase.scale_info == "A natural_minor"
        assert second_phrase.length == 4

    @pytest.mark.usefixtures("init_module")
    def test_generate_phrases_empty_progression(self):
        """Test handling of empty progression."""
        phrases = self.melody_player.generate_phrases([])
        assert len(phrases) == 0

    @pytest.mark.usefixtures("init_module")
    def test_phrase_connection(self):
        """Test that phrases are properly connected."""
        progression = [
            ("C", "major", "C", "maj7", 2),
            ("C", "major", "F", "maj7", 2),
        ]

        phrases = self.melody_player.generate_phrases(progression)

        # Get the last note of first phrase
        last_note = phrases[0].notes[-1]
        # Get the first note of second phrase
        first_note = phrases[1].notes[0]

        # Verify that the connection follows melody generator rules
        if not self.melody_generator.is_chord_tone(last_note, ["C", "E", "G", "B"]):
            # If last note wasn't a chord tone, first note should be adjacent
            adjacent_notes = self.melody_generator.get_adjacent_notes(
                last_note, ["C", "D", "E", "F", "G", "A", "B"]
            )
            assert first_note in adjacent_notes
