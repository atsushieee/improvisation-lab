"""Base class for melody practice applications."""

from abc import ABC, abstractmethod
from typing import List, Optional

import numpy as np

from improvisation_lab.config import Config
from improvisation_lab.domain.composition import PhraseData
from improvisation_lab.presentation.melody_practice import ViewTextManager
from improvisation_lab.service import MelodyPracticeService


class BaseMelodyPracticeApp(ABC):
    """Base class for melody practice applications."""

    def __init__(self, service: MelodyPracticeService, config: Config):
        """Initialize the application.

        Args:
            service: MelodyPracticeService instance.
            config: Config instance.
        """
        self.service = service
        self.config = config
        self.phrases: Optional[List[PhraseData]] = None
        self.current_phrase_idx: int = 0
        self.current_note_idx: int = 0
        self.is_running: bool = False
        self.text_manager = ViewTextManager()

    @abstractmethod
    def _process_audio_callback(self, audio_data: np.ndarray):
        """Process incoming audio data and update the application state.

        Args:
            audio_data: Audio data to process.
        """
        pass

    @abstractmethod
    def _advance_to_next_note(self):
        """Advance to the next note or phrase."""
        pass

    @abstractmethod
    def launch(self, **kwargs):
        """Launch the application.

        Args:
            **kwargs: Additional keyword arguments for the launch method.
        """
        pass
