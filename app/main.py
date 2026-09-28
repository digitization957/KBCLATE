"""Entry point: launches the KBC-style kiosk app in a fullscreen pywebview window."""
import sys

import webview

from game_api import Api
from paths import ensure_user_files, resource_path

INDEX_HTML = resource_path("web", "index.html")

_window = None


def _get_window():
    return _window


def main():
    global _window
    questions_path, log_path = ensure_user_files()
    api = Api(_get_window, questions_path, log_path)

    _window = webview.create_window(
        "Kaun Banega Luckypati",
        INDEX_HTML,
        js_api=api,
        fullscreen=True,
        confirm_close=False,
        background_color="#1a0033",
    )

    webview.start(debug="--debug" in sys.argv)


if __name__ == "__main__":
    main()
