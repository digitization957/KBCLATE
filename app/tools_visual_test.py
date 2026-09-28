"""Visual QA harness: opens the app in a normal (non-fullscreen) window,
drives it through idle -> name -> intro -> game screen via evaluate_js,
and takes OS-level screenshots at each stage. Not part of the shipped app.
"""
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
    time.sleep(2.0)
    w = _window
    screenshot("qa_1_idle")

    w.evaluate_js("document.getElementById('btn-new-contestant').click()")
    time.sleep(0.6)
    screenshot("qa_2_name")

    w.evaluate_js(
        "var i=document.getElementById('input-name'); i.value='Priya Sharma'; "
        "i.dispatchEvent(new Event('input'));"
    )
    time.sleep(0.3)
    w.evaluate_js("document.getElementById('btn-start-game').click()")
    time.sleep(0.8)
    screenshot("qa_3_intro")

    time.sleep(6.5)  # let intro auto-advance (fallback timeout is 6s)
    screenshot("qa_4_game_q1")

    # select an option to see the 'selected' highlight state
    w.evaluate_js("document.querySelector('.option-btn[data-idx=\"1\"]').click()")
    time.sleep(0.4)
    screenshot("qa_5_option_selected")

    time.sleep(1.0)
    w.destroy()


def main():
    global _window
    api = Api(_get_window, QUESTIONS_XLSX, LOG_CSV)
    _window = webview.create_window(
        "QA - Kaun Banega Luckypati", INDEX_HTML, js_api=api,
        width=1280, height=720, background_color="#1a0033",
    )
    threading.Thread(target=run_sequence, daemon=True).start()
    webview.start(debug=False)


if __name__ == "__main__":
    main()
