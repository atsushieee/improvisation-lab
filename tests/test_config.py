"""Tests for configuration module."""

import pytest
import yaml

from improvisation_lab.config import AudioConfig, Config


class TestConfig:
    @pytest.fixture
    def sample_config_file(self, tmp_path):
        """Create a sample config file for testing."""
        config_data = {
            "audio": {
                "sample_rate": 48000,
                "buffer_duration": 0.3,
                "note_duration": 4,
            },
            "selected_song": "test_song",
            "chord_progressions": {
                "test_song": [
                    ["C", "major", "C", "maj7", 4],
                ]
            },
        }
        config_file = tmp_path / "test_config.yml"
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)
        return config_file

    def test_load_config_from_file(self, sample_config_file):
        """Test loading configuration from a YAML file."""
        config = Config(config_path=sample_config_file)

        assert config.audio.sample_rate == 48000
        assert config.audio.buffer_duration == 0.3
        assert config.audio.note_duration == 4
        assert config.selected_song == "test_song"
        assert "test_song" in config.chord_progressions

    def test_load_config_with_defaults(self):
        """Test loading configuration with default values when file doesn't exist."""
        config = Config(config_path="nonexistent.yml")

        assert config.audio.sample_rate == 44100
        assert config.audio.buffer_duration == 0.2
        assert config.audio.note_duration == 1.0
        assert config.selected_song == "fly_me_to_the_moon"
        assert "fly_me_to_the_moon" in config.chord_progressions

    def test_audio_config_from_yaml(self):
        """Test creating AudioConfig from YAML data."""
        yaml_data = {
            "sample_rate": 48000,
            "buffer_duration": 0.3,
            "note_duration": 4,
        }
        audio_config = AudioConfig.from_yaml(yaml_data)

        assert audio_config.sample_rate == 48000
        assert audio_config.buffer_duration == 0.3
        assert audio_config.note_duration == 4

    def test_pitch_detector_config_from_yaml(self):
        """Test creating PitchDetector config from YAML data."""
        yaml_data = {
            "sample_rate": 44100,
            "buffer_duration": 0.2,
            "note_duration": 3,
            "pitch_detector": {
                "hop_length": 256,
                "threshold": 0.01,
                "f0_min": 100,
                "f0_max": 800,
                "device": "cpu",
            },
        }
        audio_config = AudioConfig.from_yaml(yaml_data)

        assert audio_config.pitch_detector.hop_length == 256
        assert audio_config.pitch_detector.threshold == 0.01
        assert audio_config.pitch_detector.f0_min == 100
        assert audio_config.pitch_detector.f0_max == 800
        assert audio_config.pitch_detector.device == "cpu"
        # 未指定のパラメータはデフォルト値を保持
        assert audio_config.pitch_detector.decoder_mode == "local_argmax"
