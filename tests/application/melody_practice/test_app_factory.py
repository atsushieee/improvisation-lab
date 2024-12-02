"""Tests for the MelodyPracticeAppFactory class."""

import pytest

from improvisation_lab.application.melody_practice.app_factory import \
    MelodyPracticeAppFactory
from improvisation_lab.application.melody_practice.console_app import \
    ConsoleMelodyPracticeApp
from improvisation_lab.application.melody_practice.web_app import \
    WebMelodyPracticeApp
from improvisation_lab.config import Config
from improvisation_lab.service import MelodyPracticeService


class TestMelodyPracticeAppFactory:
    @pytest.fixture
    def init_module(self):
        self.config = Config()
        self.service = MelodyPracticeService(self.config)

    @pytest.mark.usefixtures("init_module")
    def test_create_web_app(self):
        app = MelodyPracticeAppFactory.create_app("web", self.service, self.config)
        assert isinstance(app, WebMelodyPracticeApp)

    @pytest.mark.usefixtures("init_module")
    def test_create_console_app(self):
        app = MelodyPracticeAppFactory.create_app("console", self.service, self.config)
        assert isinstance(app, ConsoleMelodyPracticeApp)

    @pytest.mark.usefixtures("init_module")
    def test_create_app_invalid_type(self):
        with pytest.raises(ValueError):
            MelodyPracticeAppFactory.create_app("invalid", self.service, self.config)
