import pytest

from improvisation_lab.domain.composition.note_transposer import NoteTransposer
from improvisation_lab.domain.music_theory import Notes


class TestNoteTransposer:
    @pytest.fixture
    def init_transposer(self):
        """Initialize NoteTransposer instance for testing."""
        self.transposer = NoteTransposer()

    @pytest.mark.usefixtures("init_transposer")
    def test_calculate_target_note(self):
        """Test calculation of target note based on interval."""
        # Test cases for different intervals
        test_cases = [
            (Notes.C, 1, Notes.C_SHARP),
            (Notes.C, 4, Notes.E),
            (Notes.B, 1, Notes.C),
            (Notes.E, -1, Notes.D_SHARP),
            (Notes.C, -2, Notes.A_SHARP),
            (Notes.G, 12, Notes.G),  # One octave up
        ]

        for base_note, interval, expected_target in test_cases:
            target_note = self.transposer.transpose_note(base_note, interval)
            assert (
                target_note == expected_target
            ), f"Failed for base_note={base_note}, interval={interval}"
