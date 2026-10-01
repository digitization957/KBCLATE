"""Resolves bundled (read-only) resource paths and the writable per-user
data folder, working identically whether run as `python main.py` or as a
frozen PyInstaller .exe."""
import csv
import hashlib
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

    # The bundled bank is authoritative: whenever a new build ships a different
    # bank than the one last installed, replace the Desktop copy once (the old
    # one is kept as questions-old.xlsx). Edits made afterwards are preserved.
    template = resource_path("data", "questions.xlsx")
    with open(template, "rb") as f:
        bundled_hash = hashlib.sha256(f.read()).hexdigest()
    marker_path = os.path.join(folder, ".bank-version")
    try:
        with open(marker_path, encoding="utf-8") as f:
            installed_hash = f.read().strip()
    except OSError:
        installed_hash = None

    if not os.path.exists(questions_path) or installed_hash != bundled_hash:
        if os.path.exists(questions_path):
            try:
                shutil.copy(questions_path, os.path.join(folder, "questions-old.xlsx"))
            except OSError:
                pass
        try:
            shutil.copy(template, questions_path)
            with open(marker_path, "w", encoding="utf-8") as f:
                f.write(bundled_hash)
        except OSError:
            pass  # e.g. file open in Excel; retried next launch

    if not os.path.exists(log_path):
        # utf-8-sig (BOM) so Excel opens the CSV correctly on double-click
        # instead of garbling Devanagari contestant names.
        with open(log_path, "w", newline="", encoding="utf-8-sig") as f:
            csv.writer(f).writerow(LOG_HEADER)

    return questions_path, log_path
