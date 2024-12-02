"""Main application module for melody practice.

This module initializes and launches the melody practice application
using either a web or console interface.
"""

import argparse

from improvisation_lab.application.melody_practice import \
    MelodyPracticeAppFactory
from improvisation_lab.config import Config
from improvisation_lab.service import MelodyPracticeService


def main():
    """Run the application."""
    parser = argparse.ArgumentParser(description="Run the melody practice application")
    parser.add_argument(
        "--app_type",
        choices=["web", "console"],
        default="web",
        help="Type of application to run (web or console)",
    )
    args = parser.parse_args()

    config = Config()
    service = MelodyPracticeService(config)
    app = MelodyPracticeAppFactory.create_app(args.app_type, service, config)
    app.launch()


if __name__ == "__main__":
    main()
