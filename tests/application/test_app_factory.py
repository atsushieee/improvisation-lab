"""Tests for the MelodyPracticeAppFactory class."""

import pytest

from improvisation_lab.application.app_factory import PracticeAppFactory
from improvisation_lab.application.interval_practice import (
    ConsoleIntervalPracticeApp, WebIntervalPracticeApp)
from improvisation_lab.application.piece_practice import (
    ConsolePiecePracticeApp, WebPiecePracticeApp)
from improvisation_lab.config import Config


class TestPracticeAppFactory:
    @pytest.fixture
    def init_module(self):
        self.config = Config()

    @pytest.mark.usefixtures("init_module")
    def test_create_web_piece_app(self):
        app = PracticeAppFactory.create_app("web", "piece", self.config)
        assert isinstance(app, WebPiecePracticeApp)

    @pytest.mark.usefixtures("init_module")
    def test_create_console_piece_app(self):
        app = PracticeAppFactory.create_app("console", "piece", self.config)
        assert isinstance(app, ConsolePiecePracticeApp)

    @pytest.mark.usefixtures("init_module")
    def test_create_web_interval_app(self):
        app = PracticeAppFactory.create_app("web", "interval", self.config)
        assert isinstance(app, WebIntervalPracticeApp)

    @pytest.mark.usefixtures("init_module")
    def test_create_console_interval_app(self):
        app = PracticeAppFactory.create_app("console", "interval", self.config)
        assert isinstance(app, ConsoleIntervalPracticeApp)

    @pytest.mark.usefixtures("init_module")
    def test_create_app_invalid_app_type(self):
        with pytest.raises(ValueError):
            PracticeAppFactory.create_app("invalid", "piece", self.config)

    @pytest.mark.usefixtures("init_module")
    def test_create_app_invalid_practice_type(self):
        with pytest.raises(ValueError):
            PracticeAppFactory.create_app("web", "invalid", self.config)
