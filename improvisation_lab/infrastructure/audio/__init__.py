"""Audio infrastructure components."""

from improvisation_lab.infrastructure.audio.audio_processor import \
    AudioProcessor
from improvisation_lab.infrastructure.audio.direct_processor import \
    DirectAudioProcessor
from improvisation_lab.infrastructure.audio.web_processor import \
    WebAudioProcessor

__all__ = ["AudioProcessor", "DirectAudioProcessor", "WebAudioProcessor"]
