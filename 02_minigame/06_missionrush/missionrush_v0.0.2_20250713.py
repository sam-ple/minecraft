import minescript as m
import time
from queue import Empty
from minescript import EventQueue, EventType

TOTAL_TIME = 30  # 制限時間（秒）
bossbar_id = "minecraft:mission_timer"
is_sneaking = False

# 直前のボスバー状態保存用（無駄更新防止）
prev_bossbar_value = None
prev_bossbar_name = None

def title_subtitle(title_text, subtitle_text=None, title_color="gold", subtitle_color="aqua", delay=1):
    m.execute("title @a clear")
    m.execute(f'title @a title {{"text":"{title_text}","color":"{title_color}","bold":true}}')
    if subtitle_text and subtitle_text.strip():
        m.execute(f'title @a subtitle {{"text":"{subtitle_text}","color":"{subtitle_color}","bold":true}}')
    time.sleep(delay)

def setup_bossbar():
    m.execute(f"bossbar remove {bossbar_id}")
    m.execute(f'bossbar add {bossbar_id} {{"text":"Mission Timer","color":"yellow"}}')
    m.execute(f"bossbar set {bossbar_id} max {TOTAL_TIME}")
    m.execute(f"bossbar set {bossbar_id} value {TOTAL_TIME}")
    m.execute(f"bossbar set {bossbar_id} players @a")
    m.execute(f"bossbar set {bossbar_id} visible true")

def update_bossbar(time_left):
    global prev_bossbar_value, prev_bossbar_name
    time_left_int = int(time_left)
    # 値更新は変わった時だけ
    if prev_bossbar_value != time_left_int:
        m.execute(f"bossbar set {bossbar_id} value {time_left_int}")
        prev_bossbar_value = time_left_int
    name_text = f"Time Left: {time_left_int}s"
    # 名前更新も変わった時だけ
    if prev_bossbar_name != name_text:
        m.execute(f'bossbar set {bossbar_id} name {{"text":"{name_text}","color":"yellow"}}')
        prev_bossbar_name = name_text

def main():
    global is_sneaking
    start_time = time.time()
    setup_bossbar()
    title_subtitle("🎮 Mission", "Sneak!", delay=1)

    with EventQueue() as eq:
        eq.register_key_listener()

        while True:
            try:
                event = eq.get(timeout=0.01)
                if event.type == EventType.KEY and event.key == 340:
                    is_sneaking = (event.action == 1)
            except Empty:
                pass

            elapsed = time.time() - start_time
            time_left = max(0, TOTAL_TIME - elapsed)
            update_bossbar(time_left)

            if is_sneaking:
                title_subtitle("✅ You Sneaked!", "★", delay=1)
                m.execute(f"bossbar remove {bossbar_id}")
                return

            if elapsed > TOTAL_TIME:
                title_subtitle("💀 Time Over!", "×", delay=1)
                m.execute(f"kill {m.player_name()}")
                m.execute(f"bossbar remove {bossbar_id}")
                return

            time.sleep(0.1)

if __name__ == "__main__":
    main()
