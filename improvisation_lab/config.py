"""Configuration module for audio settings and chord progressions."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class PitchDetectorConfig:
    """Configuration settings for pitch detection."""

    sample_rate: int = 44100
    hop_length: int = 512
    decoder_mode: str = "local_argmax"
    threshold: float = 0.006
    f0_min: int = 80
    f0_max: int = 880
    interp_uv: bool = False
    device: str = "cpu"


@dataclass
class AudioConfig:
    """Configuration class for audio-related settings."""

    sample_rate: int = 44100
    buffer_duration: float = 0.2
    note_duration: float = 1.0
    pitch_detector: PitchDetectorConfig = field(default_factory=PitchDetectorConfig)

    @classmethod
    def from_yaml(cls, yaml_data: dict) -> "AudioConfig":
        """Create AudioConfig instance from YAML data."""
        config = cls(
            sample_rate=yaml_data.get("sample_rate", cls.sample_rate),
            buffer_duration=yaml_data.get("buffer_duration", cls.buffer_duration),
            note_duration=yaml_data.get("note_duration", cls.note_duration),
        )

        if "pitch_detector" in yaml_data:
            pitch_detector_data = yaml_data["pitch_detector"]
            # The sample rate must be set explicitly
            # Use the sample rate specified in the audio config
            pitch_detector_data["sample_rate"] = config.sample_rate
            config.pitch_detector = PitchDetectorConfig(**pitch_detector_data)

        return config


@dataclass
class Config:
    """Application configuration handler."""

    audio: AudioConfig
    selected_song: str
    chord_progressions: dict

    def __init__(self, config_path: str | Path = "config.yml"):
        """Initialize Config instance.

        Args:
            config_path: Path to YAML configuration file (default: 'config.yml').
        """
        self.config_path = Path(config_path)
        self._load_config()

    def _load_config(self):
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                yaml_data = yaml.safe_load(f)
                self.audio = AudioConfig.from_yaml(yaml_data.get("audio", {}))
                self.selected_song = yaml_data.get(
                    "selected_song", "fly_me_to_the_moon"
                )
                self.chord_progressions = yaml_data.get("chord_progressions", {})
        else:
            self.audio = AudioConfig()
            self.selected_song = "fly_me_to_the_moon"
            self.chord_progressions = {
                # opening 4 bars of Fly Me to the Moon
                "fly_me_to_the_moon": [
                    ("A", "natural_minor", "A", "min7", 8),
                    ("A", "natural_minor", "D", "min7", 8),
                    ("C", "major", "G", "dom7", 8),
                    ("C", "major", "C", "maj7", 4),
                    ("F", "major", "C", "dom7", 4),
                ]
            }
