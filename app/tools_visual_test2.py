"""Visual QA for the exit and winner screens (pure CSS check, drives the DOM
directly via evaluate_js rather than playing through real game logic)."""
import os
import subprocess
import tempfile
import threading
import time

import webview

from game_api import Api

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_HTML = os.path.join(BASE_DIR, "web", "index.html")
QUESTIONS_XLSX = os.path.join(BASE_DIR, "data", "questions.xlsx")
LOG_CSV = os.path.join(tempfile.gettempdir(), "kbc_qa_log.csv")

_window = None


def _get_window():
    return _window


def screenshot(name):
    path = f"C:\\Users\\Incub\\AppData\\Local\\Temp\\{name}.png"
    ps = (
        "Add-Type -AssemblyName System.Windows.Forms; "
        "Add-Type -AssemblyName System.Drawing; "
        "$b=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds; "
        "$bmp=New-Object System.Drawing.Bitmap $b.Width,$b.Height; "
        "$g=[System.Drawing.Graphics]::FromImage($bmp); "
        "$g.CopyFromScreen($b.Location,[System.Drawing.Point]::Empty,$b.Size); "
        f"$bmp.Save('{path}',[System.Drawing.Imaging.ImageFormat]::Png)"
    )
    subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps], check=False)
    print("saved", path)


def run_sequence():
    time.sleep(1.5)
    w = _window

    w.evaluate_js(
        "document.getElementById('screen-exit').classList.add('screen--active');"
        "document.getElementById('exit-outcome-label').textContent='GAME OVER';"
        "document.getElementById('exit-name').textContent='Rohit Verma';"
        "document.getElementById('exit-level').textContent='Level 2';"
        "document.getElementById('exit-points').textContent='50 points';"
    )
    time.sleep(0.5)
    screenshot("qa_exit_screen")

    w.evaluate_js(
        "document.getElementById('screen-exit').classList.remove('screen--active');"
        "document.getElementById('screen-winner').classList.add('screen--active');"
        "document.getElementById('winner-name').textContent='Rohit Verma';"
    )
    time.sleep(0.5)
    screenshot("qa_winner_screen")

    time.sleep(1.0)
    w.destroy()


def main():
    global _window
    api = Api(_get_window, QUESTIONS_XLSX, LOG_CSV)
    _window = webview.create_window(
        "QA2 - Kaun Banega Luckypati", INDEX_HTML, js_api=api,
        width=1280, height=720, background_color="#1a0033",
    )
    threading.Thread(target=run_sequence, daemon=True).start()
    webview.start(debug=False)


if __name__ == "__main__":
    main()
