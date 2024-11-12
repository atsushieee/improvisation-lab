import pytest

from improvisation_lab.domain.melody_jam import MelodyGenerator
from improvisation_lab.domain.music_theory import Scale


class TestMelodyGenerator:

    @pytest.fixture
    def init_module(self) -> None:
        """Initialization."""
        self.melody_generator = MelodyGenerator()

    @pytest.mark.usefixtures("init_module")
    def test_is_chord_tone(self):
        """Test that is_chord_tone correctly identifies chord tones."""
        test_cases = [
            ("C", ["C", "E", "G"], True),
            ("D", ["C", "E", "G"], False),
            ("E", ["C", "E", "G", "B"], True),
            ("F", ["C", "E", "G", "B"], False),
            ("G#", ["G#", "C", "D#"], True),
            ("A", ["G#", "C", "D#"], False),
        ]

        for note, chord_tones, expected in test_cases:
            assert self.melody_generator.is_chord_tone(note, chord_tones) == expected

    @pytest.mark.usefixtures("init_module")
    def test_get_adjacent_notes(self):
        """Test that get_adjacent_notes returns correct adjacent notes."""
        test_cases = [
            ("C", ["C", "D", "E", "F", "G", "A", "B"], ["B", "D"]),
            ("C#", ["C", "D", "E", "F", "G", "A", "B"], ["C", "D"]),
            ("B", ["C", "D", "E", "F", "G", "A", "B"], ["A", "C"]),
        ]

        for note, scale_notes, expected in test_cases:
            result = self.melody_generator.get_adjacent_notes(note, scale_notes)
            assert sorted(result) == sorted(expected)

    @pytest.mark.usefixtures("init_module")
    def test_find_closest_note_in_direction(self):
        """Test that _find_closest_note_in_direction finds correct notes."""
        test_cases = [
            (
                "C",
                ["C", "D", "E", "F", "G", "A", "B"],
                1,  # direction (higher)
                "D",  # expected
            ),
            ("C#", ["C", "D", "E", "F", "G", "A", "B"], -1, "C"),  # direction (lower)
            ("B", ["C", "D", "E", "F", "G", "A", "A#"], 1, "C"),  # direction (lower)
        ]

        for note, scale_notes, direction, expected in test_cases:
            result = self.melody_generator._find_closest_note_in_direction(
                note, scale_notes, direction
            )
            assert result == expected

    @pytest.mark.usefixtures("init_module")
    def test_get_next_note(self):
        """Test that get_next_note returns correct next note based on chord tones."""
        scale_notes = ["C", "D", "E", "F", "G", "A", "A#"]

        # Case 1: Current note is a chord tone
        current_note = "C"
        chord_tones = ["C", "E", "G", "A#"]  # C7

        # Run multiple times to ensure random selection works correctly
        for _ in range(10):
            result = self.melody_generator.get_next_note(
                current_note, scale_notes, chord_tones
            )
            # Should be able to move to any scale note except current note
            assert result in scale_notes
            assert result != current_note

        # Case 2: Current note is not a chord tone
        current_note = "D"  # Not in C major triad
        expected_adjacent = ["C", "E"]  # Only adjacent notes in scale

        # Run multiple times to ensure random selection works correctly
        for _ in range(10):
            result = self.melody_generator.get_next_note(
                current_note, scale_notes, chord_tones
            )
            # Should only move to adjacent notes
            assert result in expected_adjacent

        # Case 3: Edge case - note at the end of scale
        current_note = "B"
        chord_tones = ["A", "C", "E", "G"]  # Am7
        expected_adjacent = ["A#", "C"]

        for _ in range(10):
            result = self.melody_generator.get_next_note(
                current_note, scale_notes, chord_tones
            )
            assert result in expected_adjacent

    @pytest.mark.usefixtures("init_module")
    def test_select_first_note(self):
        """Test that select_first_note returns correct first note.

        Tests the selection of the first note based on previous note and conditions.
        """
        scale_notes = ["C", "D", "E", "F", "G", "A", "B"]
        chord_tones = ["C", "E", "G"]  # C major triad

        # Case 1: prev_note is None
        for _ in range(10):
            result = self.melody_generator.select_first_note(scale_notes, chord_tones)
            assert result in scale_notes

        # Case 2: prev_note exists and was a chord tone
        prev_note = "E"
        for _ in range(10):
            result = self.melody_generator.select_first_note(
                scale_notes,
                chord_tones,
                prev_note=prev_note,
                prev_note_was_chord_tone=True,
            )
            assert result in scale_notes
            assert result != prev_note

        # Case 3: prev_note exists, wasn't a chord tone, but is in current chord tones
        prev_note = "C"
        for _ in range(10):
            result = self.melody_generator.select_first_note(
                scale_notes,
                chord_tones,
                prev_note=prev_note,
                prev_note_was_chord_tone=False,
            )
            assert result in scale_notes
            assert result != prev_note

        # Case 4: prev_note exists, wasn't a chord tone and isn't in current chord tones
        prev_note = "C#"
        expected_adjacent = ["C", "D"]  # Adjacent notes in scale
        for _ in range(10):
            result = self.melody_generator.select_first_note(
                scale_notes,
                chord_tones,
                prev_note=prev_note,
                prev_note_was_chord_tone=False,
            )
            assert result in expected_adjacent

    @pytest.mark.usefixtures("init_module")
    def test_generate_phrase(self):
        """Test that generate_phrase generates valid melody phrases."""
        # Case 1: First phrase (no previous note)
        phrase = self.melody_generator.generate_phrase(
            scale_root="C",
            scale_type="major",
            chord_root="C",
            chord_type="maj7",
            length=8,
        )
        assert len(phrase) == 8
        assert all(note in Scale.get_scale_notes("C", "major") for note in phrase)

        # Case 2: Phrase after a chord tone
        phrase = self.melody_generator.generate_phrase(
            scale_root="A",
            scale_type="natural_minor",
            chord_root="A",
            chord_type="min7",
            prev_note="A",
            prev_note_was_chord_tone=True,
            length=6,
        )
        assert len(phrase) == 6
        assert all(
            note in Scale.get_scale_notes("A", "natural_minor") for note in phrase
        )

        # Case 3: Phrase after a non-chord tone
        for _ in range(10):
            phrase = self.melody_generator.generate_phrase(
                scale_root="D",
                scale_type="harmonic_minor",
                chord_root="A",
                chord_type="dom7",
                prev_note="G#",
                prev_note_was_chord_tone=False,
                length=4,
            )
            assert len(phrase) == 4
            scale_notes = Scale.get_scale_notes("D", "harmonic_minor")
            assert phrase[0] == "G" or phrase[0] == "A"
            assert all(note in scale_notes for note in phrase)

        # Case 4: Different lengths
        for length in [4, 8, 12]:
            phrase = self.melody_generator.generate_phrase(
                scale_root="G",
                scale_type="major",
                chord_root="G",
                chord_type="maj7",
                length=length,
            )
            assert len(phrase) == length
