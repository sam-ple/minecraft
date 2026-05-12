import minescript as m
from minescript import EventQueue, EventType
import datetime

LOG_FILE = "chat_log.txt"

def log_message(msg: str):
    """Append chat messages to a log file"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")

eq = EventQueue()
eq.register_chat_listener()
m.echo("Chat listener ready! Logging ALL chat messages...")

while True:
    event = eq.get()
    if not event or event.type != EventType.CHAT:
        continue

    msg = event.message
    log_message(msg)
