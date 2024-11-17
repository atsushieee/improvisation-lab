"""Module for melody improvisation generation."""

from improvisation_lab.domain.composition.melody_composer import (
    MelodyComposer, PhraseData)
from improvisation_lab.domain.composition.phrase_generator import \
    PhraseGenerator

__all__ = ["PhraseGenerator", "PhraseData", "MelodyComposer"]
