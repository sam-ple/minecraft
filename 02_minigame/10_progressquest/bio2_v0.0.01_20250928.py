import minescript as m
from minescript import EventQueue, EventType
import re
import os

player = m.player_name()
BIO_FILE = "bio_output.txt"
visited = set()

# 既存の visited 読み込み
if os.path.exists(BIO_FILE):
    with open(BIO_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content:
            visited = set(content.split(","))

# チャットで初訪問バイオームを検出
first_visit_pattern = re.compile(r"🌍 First visit: (\w+)")

def save_visited():
    with open(BIO_FILE, "w", encoding="utf-8") as f:
        f.write(",".join(sorted(visited)))

# EventQueue はメインスレッドで保持
with EventQueue() as eq:
    eq.register_chat_listener()
    m.echo("🌍 BiomeTracker running...")

    while True:
        event = eq.get()
        if not event or event.type != EventType.CHAT:
            continue
        msg = event.message.strip()
        if msg.startswith("<") and ">" in msg:
            msg = msg.split(">", 1)[1].strip()
        match = first_visit_pattern.search(msg)
        if match:
            biome = match.group(1)
            if biome not in visited:
                visited.add(biome)
                save_visited()
                m.echo(f"✅ Saved first visit biome: {biome}")
