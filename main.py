"""Main application module for melody practice.

This module initializes and launches the melody practice application
using either a web or console interface.
"""

import argparse

import gradio as gr

from improvisation_lab.application import PracticeAppFactory
from improvisation_lab.config import Config


def create_practice_interface(practice_type: str) -> gr.Blocks:
    """Create a practice interface for the given practice type.

    Args:
        practice_type: The type of practice to create an interface for.

    Returns:
        gr.Blocks: The practice interface.
    """
    config = Config()
    app = PracticeAppFactory.create_app("web", practice_type, config)
    return app.ui._build_interface()


def main():
    """Run the application."""
    parser = argparse.ArgumentParser(description="Run the melody practice application")
    parser.add_argument(
        "--app_type",
        choices=["web", "console"],
        default="web",
        help="Type of application to run (web or console)",
    )
    parser.add_argument(
        "--practice_type",
        choices=["interval", "piece"],
        default="interval",
        help="Type of practice to run (interval or piece)",
    )
    args = parser.parse_args()

    if args.app_type == "web":
        with gr.Blocks(
            head="""
            <script src="https://cdn.jsdelivr.net/npm/tone@14.8.39/build/Tone.js">
            </script>
        """
        ) as app:
            with gr.Tabs():
                with gr.TabItem("Interval Practice"):
                    create_practice_interface("interval")
                with gr.TabItem("Piece Practice"):
                    create_practice_interface("piece")
        app.launch()
    else:
        config = Config()
        app = PracticeAppFactory.create_app(args.app_type, args.practice_type, config)
        app.launch()


if __name__ == "__main__":
    main()
