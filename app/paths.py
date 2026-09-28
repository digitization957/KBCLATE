"""Resolves bundled (read-only) resource paths and the writable per-user
data folder, working identically whether run as `python main.py` or as a
frozen PyInstaller .exe."""
import csv
import os
import shutil
import sys

DATA_FOLDER_NAME = "Kaun Banega Luckypati"
LOG_HEADER = [
    "timestamp", "name", "outcome", "level_reached",
    "points", "lifeline_used", "last_question_number",
]


def resource_path(*parts):
    """Path to a bundled read-only resource (web assets, template files)."""
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS  # PyInstaller onefile extraction dir
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, *parts)


def _real_desktop_path():
    """Windows redirects Desktop to OneDrive on many machines, so the real
    path is often NOT %USERPROFILE%\\Desktop. Ask the registry (the same
    place Explorer itself reads) instead of guessing."""
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
        )
        value, _ = winreg.QueryValueEx(key, "Desktop")
        winreg.CloseKey(key)
        return os.path.expandvars(value)
    except OSError:
        return None


def user_data_dir():
    """The writable folder on the Desktop that holds questions.xlsx and
    game-log.csv. Created on first run; safe to call every launch."""
    desktop = _real_desktop_path()
    if not desktop or not os.path.isdir(desktop):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.isdir(desktop):
        desktop = os.path.expanduser("~")
    folder = os.path.join(desktop, DATA_FOLDER_NAME)
    os.makedirs(folder, exist_ok=True)
    return folder


def ensure_user_files():
    """First-run setup: seeds an empty questions.xlsx template and an empty
    game-log.csv (header only) into the user data folder if not already
    present. Returns (questions_path, log_path)."""
    folder = user_data_dir()
    questions_path = os.path.join(folder, "questions.xlsx")
    log_path = os.path.join(folder, "game-log.csv")

    if not os.path.exists(questions_path):
        template = resource_path("data", "questions.xlsx")
        shutil.copy(template, questions_path)

    if not os.path.exists(log_path):
        with open(log_path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(LOG_HEADER)

    return questions_path, log_path
