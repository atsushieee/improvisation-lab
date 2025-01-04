"""Module for handling melody generation and playback."""

from dataclasses import dataclass
from typing import List, Optional

from improvisation_lab.domain.composition.note_transposer import NoteTransposer
from improvisation_lab.domain.composition.phrase_generator import \
    PhraseGenerator
from improvisation_lab.domain.music_theory import ChordTone, Notes


@dataclass
class PhraseData:
    """Data structure containing information about a melodic phrase."""

    notes: List[str]
    chord_name: str
    scale_info: str
    length: int


class MelodyComposer:
    """Class responsible for generating melodic phrases based on chord progressions."""

    def __init__(self):
        """Initialize MelodyPlayer with a melody generator."""
        self.phrase_generator = PhraseGenerator()
        self.note_transposer = NoteTransposer()

    def generate_phrases(
        self, progression: List[tuple[str, str, str, str, int]]
    ) -> List[PhraseData]:
        """Generate a sequence of melodic phrases based on a chord progression.

        Args:
            progression:
                List of tuples containing (scale_root, scale_type, chord_root,
                chord_type, length) for each chord in the progression.

        Returns:
            List of PhraseData objects containing the generated melodic phrases.
        """
        phrases: List[PhraseData] = []
        prev_note: Optional[str] = None
        prev_note_was_chord_tone = False

        for scale_root, scale_type, chord_root, chord_type, length in progression:
            phrase = self.phrase_generator.generate_phrase(
                scale_root=scale_root,
                scale_type=scale_type,
                chord_root=chord_root,
                chord_type=chord_type,
                prev_note=prev_note,
                prev_note_was_chord_tone=prev_note_was_chord_tone,
                length=length,
            )

            # Update information for the next phrase
            prev_note = phrase[-1]
            prev_note_was_chord_tone = self.phrase_generator.is_chord_tone(
                prev_note, ChordTone.get_chord_tones(chord_root, chord_type)
            )

            phrases.append(
                PhraseData(
                    notes=phrase,
                    chord_name=f"{chord_root}{chord_type}",
                    scale_info=f"{scale_root} {scale_type}",
                    length=length,
                )
            )

        return phrases

    def generate_interval_melody(
        self, base_notes: List[Notes], interval: int
    ) -> List[List[Notes]]:
        """Generate a melody based on interval transitions.

        Args:
            base_notes: List of base notes to start from.
            interval: Interval to move to and back.

        Returns:
            List of lists containing the generated melody.
        """
        melody = []
        for base_note in base_notes:
            target_note = self.note_transposer.transpose_note(base_note, interval)
            melody.append([base_note, target_note, base_note])
        return melody
