"""Module for generating improvised melody phrases.

This module provides functionality to generate natural melody phrases
based on given scales and chord progressions, following music theory principles.
"""

import random

from improvisation_lab.domain.music_theory import ChordTone, Notes, Scale


class MelodyGenerator:
    """Class for generating improvised melody phrases.

    This class generates melody phrases based on given scales and chord progressions,
    following music theory rules.
    The next note selection depends on whether the current note is a chord tone or not,
    with chord tones having more freedom in movement
    while non-chord tones move to adjacent notes.
    """

    def is_chord_tone(self, note: str, chord_tones: list[str]) -> bool:
        """Check if a note is a chord tone.

        Args:
            note: The note to check.
            chord_tones: The list of chord tones.

        Returns:
            True if the note is a chord tone, False otherwise.
        """
        return note in chord_tones

    def get_adjacent_notes(self, note: str, scale_notes: list[str]) -> list[str]:
        """Get adjacent notes to a given note.

        Args:
            note: The note to get adjacent notes to.
            scale_notes: The list of notes in the scale.

        Returns:
            The list of adjacent notes in order (lower note first, then higher note).
        """
        length_scale_notes = len(scale_notes)
        if note in scale_notes:
            note_index = scale_notes.index(note)
            return [
                scale_notes[(note_index - 1) % length_scale_notes],
                scale_notes[(note_index + 1) % length_scale_notes],
            ]

        return [
            self._find_closest_note_in_direction(note, scale_notes, -1),
            self._find_closest_note_in_direction(note, scale_notes, 1),
        ]

    def _find_closest_note_in_direction(
        self, note: str, scale_notes: list[str], direction: int
    ) -> str:
        """Find the closest note in a given direction within the scale.

        Args:
            start_index: Starting index in the chromatic scale.
            all_notes: List of all notes (chromatic scale).
            scale_notes: List of notes in the target scale.
            direction: Direction to search (-1 for lower, 1 for higher).

        Returns:
            The closest note in the given direction that exists in the scale.
        """
        all_notes = [note.value for note in Notes]  # Chromatic scale
        note_index = all_notes.index(note)

        current_index = note_index
        while True:
            current_index = (current_index + direction) % 12
            current_note = all_notes[current_index]
            if current_note in scale_notes:
                return current_note
            if current_index == note_index:  # If we've gone full circle
                break
        return all_notes[current_index]

    def get_next_note(
        self, current_note: str, scale_notes: list[str], chord_tones: list[str]
    ) -> str:
        """Get the next note based on the current note, scale, and chord tones.

        Args:
            current_note: The current note.
            scale_notes: The list of notes in the scale.
            chord_tones: The list of chord tones.

        Returns:
            The next note.
        """
        is_current_chord_tone = self.is_chord_tone(current_note, chord_tones)

        if is_current_chord_tone:
            # For chord tones, freely move to any scale note
            available_notes = [note for note in scale_notes if note != current_note]
            return random.choice(available_notes)
        # For non-chord tones, move to adjacent notes only
        adjacent_notes = self.get_adjacent_notes(current_note, scale_notes)
        return random.choice(adjacent_notes)

    def select_first_note(
        self,
        scale_notes: list[str],
        chord_tones: list[str],
        prev_note: str | None = None,
        prev_note_was_chord_tone: bool = False,
    ) -> str:
        """Select the first note of a phrase.

        Args:
            scale_notes: The list of notes in the scale.
            chord_tones: The list of chord tones.
            prev_note: The last note of the previous phrase (default: None).
            prev_note_was_chord_tone:
                Whether the previous note was a chord tone (default: False).

        Returns:
            The selected first note.
        """
        # For the first phrase, randomly select from scale notes
        if prev_note is None:
            return random.choice(scale_notes)

        # Case: previous note was a chord tone, can move freely
        if prev_note_was_chord_tone:
            available_notes = [note for note in scale_notes if note != prev_note]
            return random.choice(available_notes)

        # Case: previous note was not a chord tone
        if prev_note in chord_tones:
            # If it's a chord tone in the current chord, can move freely
            available_notes = [note for note in scale_notes if note != prev_note]
            return random.choice(available_notes)

        # If it's not a chord tone, can only move to adjacent notes
        adjacent_notes = self.get_adjacent_notes(prev_note, scale_notes)
        return random.choice(adjacent_notes)

    def generate_phrase(
        self,
        scale_root: str,
        scale_type: str,
        chord_root: str,
        chord_type: str,
        prev_note: str | None = None,
        prev_note_was_chord_tone: bool = False,
        length=8,
    ) -> list[str]:
        """Generate a phrase of notes.

        Args:
            scale_root: The root note of the scale.
            scale_type: The type of scale (e.g., "major", "natural_minor").
            chord_root: The root note of the chord.
            chord_type: The type of chord (e.g., "maj", "maj7").
            prev_note: The last note of the previous phrase (default: None).
            prev_note_was_chord_tone:
                Whether the previous note was a chord tone (default: False).
            length: The length of the phrase (default: 8).

        Returns:
            A list of note names in the phrase.
        """
        # Get scale notes and chord tones
        scale_notes = Scale.get_scale_notes(scale_root, scale_type)
        chord_tones = ChordTone.get_chord_tones(chord_root, chord_type)

        # Generate the phrase
        phrase = []

        # Select the first note
        current_note = self.select_first_note(
            scale_notes, chord_tones, prev_note, prev_note_was_chord_tone
        )
        phrase.append(current_note)

        # Generate remaining notes
        for _ in range(length - 1):
            current_note = self.get_next_note(current_note, scale_notes, chord_tones)
            phrase.append(current_note)

        return phrase
