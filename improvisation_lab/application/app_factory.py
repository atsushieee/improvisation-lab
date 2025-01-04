"""Factory class for creating melody practice applications."""

from improvisation_lab.application.interval_practice import (
    ConsoleIntervalPracticeApp, WebIntervalPracticeApp)
from improvisation_lab.application.piece_practice import (
    ConsolePiecePracticeApp, WebPiecePracticeApp)
from improvisation_lab.config import Config
from improvisation_lab.service import (IntervalPracticeService,
                                       PiecePracticeService)


class PracticeAppFactory:
    """Factory class for creating melody practice applications."""

    @staticmethod
    def create_app(app_type: str, practice_type: str, config: Config):
        """Create a melody practice application.

        Args:
            app_type: Type of application to create.
            practice_type: Type of practice to create.
            config: Config instance.
        """
        if app_type == "web":
            if practice_type == "piece":
                service = PiecePracticeService(config)
                return WebPiecePracticeApp(service, config)
            elif practice_type == "interval":
                service = IntervalPracticeService(config)
                return WebIntervalPracticeApp(service, config)
            else:
                raise ValueError(f"Unknown practice type: {practice_type}")
        elif app_type == "console":
            if practice_type == "piece":
                service = PiecePracticeService(config)
                return ConsolePiecePracticeApp(service, config)
            elif practice_type == "interval":
                service = IntervalPracticeService(config)
                return ConsoleIntervalPracticeApp(service, config)
            else:
                raise ValueError(f"Unknown practice type: {practice_type}")
        else:
            raise ValueError(f"Unknown app type: {app_type}")
