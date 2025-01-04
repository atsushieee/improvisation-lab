"""Note transposer."""

from improvisation_lab.domain.music_theory import Notes


class NoteTransposer:
    """Class responsible for transposing notes."""

    def __init__(self):
        """Initialize NoteTransposer."""
        pass

    def transpose_note(self, note: Notes, interval: int) -> Notes:
        """Transpose a note by a given interval."""
        chromatic_scale = Notes.get_chromatic_scale(note.value)
        transposed_index = (interval) % len(chromatic_scale)
        return Notes(chromatic_scale[transposed_index])
