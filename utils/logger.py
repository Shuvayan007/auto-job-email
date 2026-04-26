import os
from datetime import datetime


def log_event(session_dir, message):
    log_file = os.path.join(session_dir, "session.log")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")