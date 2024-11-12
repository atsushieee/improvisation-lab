"""Tests for music theory related classes."""

import pytest

from improvisation_lab.domain.music_theory import ChordTone, Notes, Scale


class TestNotes:
    def test_notes_values_are_valid(self):
        """Test that initializing Notes with invalid note name raises ValueError."""
        with pytest.raises(ValueError):
            Notes("H")

    def test_get_note_index_returns_correct_index(self):
        assert Notes.get_note_index("C") == 0
        assert Notes.get_note_index("G") == 7

    def test_get_chromatic_scale_returns_ordered_notes(self):
        """Test that get_chromatic_scale returns notes in chromatic order."""
        assert Notes.get_chromatic_scale("C") == [
            "C",
            "C#",
            "D",
            "D#",
            "E",
            "F",
            "F#",
            "G",
            "G#",
            "A",
            "A#",
            "B",
        ]
        assert Notes.get_chromatic_scale("G") == [
            "G",
            "G#",
            "A",
            "A#",
            "B",
            "C",
            "C#",
            "D",
            "D#",
            "E",
            "F",
            "F#",
        ]

    def test_get_chromatic_scale_raises_error_for_invalid_note(self):
        """Test that get_chromatic_scale raises ValueError for invalid notes."""
        with pytest.raises(ValueError):
            Notes.get_chromatic_scale("Z")


class TestScale:
    def test_get_scale_notes_returns_correct_notes(self):
        assert Scale.get_scale_notes("A", "major") == [
            "A",
            "B",
            "C#",
            "D",
            "E",
            "F#",
            "G#",
        ]


class TestChordTone:
    """Tests for ChordTone class."""

    def test_get_chord_tones_returns_correct_notes(self):
        """Test that get_chord_tones returns correct chord tones."""
        test_cases = [
            ("C", "maj", ["C", "E", "G", "A"]),
            ("D", "min7", ["D", "F", "A", "C"]),
            ("G", "dom7", ["G", "B", "D", "F"]),
            ("A", "dim7", ["A", "C", "D#", "F#"]),
            ("F", "maj7", ["F", "A", "C", "E"]),
            ("B", "min7(b5)", ["B", "D", "F", "A"]),
        ]

        for root, chord_type, expected in test_cases:
            assert ChordTone.get_chord_tones(root, chord_type) == expected
