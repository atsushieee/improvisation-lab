"""Tests for melody composer module."""

import pytest

from improvisation_lab.domain.composition.melody_composer import MelodyComposer
from improvisation_lab.domain.music_theory import Notes


class TestMelodyComposer:
    @pytest.fixture
    def init_module(self):
        """Initialize test module."""
        self.melody_composer = MelodyComposer()

    @pytest.mark.usefixtures("init_module")
    def test_generate_phrases_basic(self):
        """Test basic phrase generation functionality."""
        progression = [
            ("C", "major", "C", "maj7", 4),
            ("A", "natural_minor", "A", "min7", 4),
        ]

        phrases = self.melody_composer.generate_phrases(progression)

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
        phrases = self.melody_composer.generate_phrases([])
        assert len(phrases) == 0

    @pytest.mark.usefixtures("init_module")
    def test_phrase_connection(self):
        """Test that phrases are properly connected."""
        progression = [
            ("C", "major", "C", "maj7", 2),
            ("C", "major", "F", "maj7", 2),
        ]

        # Get chord tones for both chords
        first_chord_tones = ["C", "E", "G", "B"]  # Cmaj7
        second_chord_tones = ["F", "A", "C", "E"]  # Fmaj7

        # Run multiple times to ensure random selection works correctly
        for _ in range(10):
            phrases = self.melody_composer.generate_phrases(progression)

            # Get the last note of first phrase
            last_note = phrases[0].notes[-1]
            # Get the first note of second phrase
            first_note = phrases[1].notes[0]

            # Check if the last note is a chord tone of either chord
            is_first_chord_tone = self.melody_composer.phrase_generator.is_chord_tone(
                last_note, first_chord_tones
            )
            is_second_chord_tone = self.melody_composer.phrase_generator.is_chord_tone(
                last_note, second_chord_tones
            )

            # If the last note is not a chord tone of either chord
            if not is_first_chord_tone and not is_second_chord_tone:
                # Then first note should be adjacent
                adjacent_notes = (
                    self.melody_composer.phrase_generator.get_adjacent_notes(
                        last_note, ["C", "D", "E", "F", "G", "A", "B"]
                    )
                )
                assert first_note in adjacent_notes

    @pytest.mark.usefixtures("init_module")
    def test_generate_interval_melody(self):
        """Test interval melody generation."""
        base_notes = [Notes.C, Notes.E, Notes.G, Notes.B]
        interval = 2

        melody = self.melody_composer.generate_interval_melody(base_notes, interval)

        # Check the length of the melody
        assert len(melody) == len(base_notes)
        assert len(melody[0]) == 3

        # Check the structure of the melody
        for i, base_note in enumerate(base_notes):
            assert melody[i][0] == base_note
            transposed_note = self.melody_composer.note_transposer.transpose_note(
                base_note, interval
            )
            assert melody[i][1] == transposed_note
            assert melody[i][2] == base_note
