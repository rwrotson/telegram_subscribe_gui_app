from pathlib import Path

PREFS_FOLDER = Path("~/.telegram_subscribe_app").expanduser()
USER_FILE_PATH = PREFS_FOLDER / "user.txt"
CHANNEL_FILE_PATH = PREFS_FOLDER / "channels.txt"
SESSION_FILE_PATH = PREFS_FOLDER / "session"
