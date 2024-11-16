"""Module for melody improvisation generation."""

from improvisation_lab.domain.melody_jam.melody_composer import (
    MelodyComposer, PhraseData)
from improvisation_lab.domain.melody_jam.phrase_generator import \
    PhraseGenerator

__all__ = ["PhraseGenerator", "PhraseData", "MelodyComposer"]
