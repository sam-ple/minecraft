# ============================================================
# Chat Log Toggle (Simple)
# Right Shift = Start / Stop logging
# ============================================================

import minescript as m
from minescript import EventQueue, EventType
import datetime
import os

# =========================
# config
# =========================

KEY_CODE = 344  # Right Shift

BASE_DIR = "minescript/data/chatlog"
os.makedirs(BASE_DIR, exist_ok=True)

LOG_FILE = f"{BASE_DIR}/chatlog.txt"

logging_enabled = False


# =========================
# log function
# =========================

def log_message(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")


# =========================
# main
# =========================

with EventQueue() as eq:

    eq.register_chat_listener()
    eq.register_key_listener()

    m.echo("📜 Chat Logger Ready")
    m.echo("➡ Right Shift = Toggle Logging")

    while True:

        event = eq.get()

        # --- key toggle ---
        if event.type == EventType.KEY and event.action == 0 and event.key == KEY_CODE:

            logging_enabled = not logging_enabled

            if logging_enabled:
                m.echo("🟢 Chat logging START")
            else:
                m.echo("🔴 Chat logging STOP")

        # --- chat log ---
        if event.type == EventType.CHAT and logging_enabled:
            log_message(event.message)
