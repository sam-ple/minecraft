import minescript as m
import time
from queue import Empty
from minescript import EventQueue, EventType

TOTAL_TIME = 30  # Time limit in seconds
is_sneaking = False

def title_subtitle(title_text, subtitle_text=None, title_color="gold", subtitle_color="aqua", delay=1):
    m.execute("title @a clear")
    m.execute(f'title @a title {{"text":"{title_text}","color":"{title_color}","bold":true}}')
    if subtitle_text and subtitle_text.strip():
        m.execute(f'title @a subtitle {{"text":"{subtitle_text}","color":"{subtitle_color}","bold":true}}')
    time.sleep(delay)

def main():
    global is_sneaking
    start_time = time.time()
    title_subtitle("🎮 Mission: Sneak!", "☆", delay=1)

    with EventQueue() as eq:
        eq.register_key_listener()

        while True:
            try:
                # Detect left Shift key (key code 340)
                event = eq.get(timeout=0.01)
                if event.type == EventType.KEY and event.key == 340:
                    is_sneaking = (event.action == 1)
            except Empty:
                pass

            if is_sneaking:
                title_subtitle("✅ Sneak detected!", "★", delay=1)
                return

            if time.time() - start_time > TOTAL_TIME:
                title_subtitle("💀 Time's up!", "×", delay=1)
                m.execute(f"kill {m.player_name()}")
                return

            time.sleep(0.1)

if __name__ == "__main__":
    main()
