"""Factory class for creating melody practice applications."""

from improvisation_lab.application.melody_practice.console_app import \
    ConsoleMelodyPracticeApp
from improvisation_lab.application.melody_practice.web_app import \
    WebMelodyPracticeApp
from improvisation_lab.config import Config
from improvisation_lab.service import MelodyPracticeService


class MelodyPracticeAppFactory:
    """Factory class for creating melody practice applications."""

    @staticmethod
    def create_app(app_type: str, service: MelodyPracticeService, config: Config):
        """Create a melody practice application.

        Args:
            app_type: Type of application to create.
            service: MelodyPracticeService instance.
            config: Config instance.
        """
        if app_type == "web":
            return WebMelodyPracticeApp(service, config)
        elif app_type == "console":
            return ConsoleMelodyPracticeApp(service, config)
        else:
            raise ValueError(f"Unknown app type: {app_type}")
