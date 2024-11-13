"""Module containing basic music theory concepts and constants."""

from enum import Enum

import numpy as np


class Notes(str, Enum):
    """Enumeration of musical notes in chromatic scale.

    This class represents the twelve notes of the chromatic scale
    and provides methods for note manipulation and validation.
    It inherits from both str and Enum to provide string-like behavior
    while maintaining the benefits of enumeration.

    The str inheritance allows direct string operations on the note values,
    while Enum ensures type safety and provides a defined set of valid notes.

    Examples:
        >>> note = Notes.C
        >>> isinstance(note, str)  # True
        >>> note.lower()  # 'c'
        >>> note + 'm'    # 'Cm'
    """

    C = "C"
    C_SHARP = "C#"
    D = "D"
    D_SHARP = "D#"
    E = "E"
    F = "F"
    F_SHARP = "F#"
    G = "G"
    G_SHARP = "G#"
    A = "A"
    A_SHARP = "A#"
    B = "B"

    @classmethod
    def get_note_index(cls, note: str) -> int:
        """Get the index of a note in the chromatic scale.

        Args:
            note (str): The note name to find the index for.

        Returns:
            int: The index of the note in the chromatic scale (0-11).
        """
        return list(cls).index(cls(note))

    @classmethod
    def get_chromatic_scale(cls, note: str) -> list[str]:
        """Return all notes in chromatic order.

        Args:
            note (str): The note name to start the chromatic scale from.

        Returns:
            list[str]: A list of note names in chromatic order,
                      starting from C (e.g., ["C", "C#", "D", ...]).
        """
        start_idx = cls.get_note_index(note)
        all_notes = [note.value for note in cls]
        return all_notes[start_idx:] + all_notes[:start_idx]

    @classmethod
    def convert_frequency_to_note(cls, frequency: float) -> str:
        """Convert a frequency in Hz to the nearest note name on a piano keyboard.

        Args:
            frequency: The frequency in Hz.

        Returns:
            The name of the nearest note.
        """
        A4_frequency = 440.0
        # Calculate the number of semitones from A4 (440Hz)
        n = 12 * np.log2(frequency / A4_frequency)

        # Round to the nearest semitone
        n = round(n)

        # Calculate octave and index of note name with respect to A4
        octave = 4 + (n + 9) // 12
        note_idx = (n + 9) % 12

        note = cls.get_chromatic_scale(cls.C)[note_idx]
        return f"{note}{octave}"


class Scale:
    """Musical scale representation and operations.

    This class handles scale-related operations including scale generation
    and scale note calculations.
    """

    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "natural_minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    }

    @classmethod
    def get_scale_notes(cls, root_note: str, scale_type: str) -> list[str]:
        """Generate scale notes from root note and scale type.

        Args:
            root_note: The root note of the scale.
            scale_type: The type of scale (e.g., "major", "natural_minor").

        Returns:
            A list of note names in the scale.

        Raises:
            ValueError: If root_note is invalid or scale_type is not recognized.
        """
        if scale_type not in cls.SCALES:
            raise ValueError(f"Invalid scale type: {scale_type}")

        scale_pattern = cls.SCALES[scale_type]
        chromatic = Notes.get_chromatic_scale(root_note)
        return [chromatic[interval % 12] for interval in scale_pattern]


class ChordTone:
    """Musical chord tone representation and operations.

    This class handles chord tone-related operations
    including chord tone generation and chord tone calculation.
    """

    CHORD_TONES = {
        "maj": [0, 4, 7, 9],
        "maj7": [0, 4, 7, 11],
        "min7": [0, 3, 7, 10],
        "min7(b5)": [0, 3, 6, 10],
        "dom7": [0, 4, 7, 10],
        "dim7": [0, 3, 6, 9],
    }

    @classmethod
    def get_chord_tones(cls, root_note: str, chord_type: str) -> list[str]:
        """Generate chord tones from root note and chord type.

        Args:
            root_note: The root note of the chord.
            chord_type: The type of chord (e.g., "maj", "maj7").

        Returns:
            A list of note names in the chord.
        """
        if chord_type not in cls.CHORD_TONES:
            raise ValueError(f"Invalid chord type: {chord_type}")

        chord_pattern = cls.CHORD_TONES[chord_type]
        chromatic = Notes.get_chromatic_scale(root_note)
        return [chromatic[interval] for interval in chord_pattern]
