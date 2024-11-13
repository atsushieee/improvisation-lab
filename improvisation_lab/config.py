"""Configuration module for audio settings and chord progressions."""

from dataclasses import dataclass


@dataclass
class AudioConfig:
    """Configuration class for audio-related settings."""

    SAMPLE_RATE: int = 44100
    BUFFER_DURATION: float = 0.2
    NOTE_DURATION: int = 3  # seconds per note


class ChordProgression:
    """Collection of predefined chord progressions used in the application."""

    # (scale_root, scale_type, chord_root, chord_type, length)
    FLY_ME_TO_THE_MOON = [
        ("A", "natural_minor", "A", "min7", 8),
        ("A", "natural_minor", "D", "min7", 8),
        ("C", "major", "G", "dom7", 8),
        ("C", "major", "C", "maj7", 4),
        ("F", "major", "C", "dom7", 4),
        ("C", "major", "F", "maj7", 8),
        ("A", "natural_minor", "B", "min7(b5)", 8),
        ("A", "harmonic_minor", "E", "dom7", 8),
        ("A", "natural_minor", "A", "min7", 4),
        ("D", "harmonic_minor", "A", "dom7", 4),
    ]
