import minescript as m
import time
import threading
from minescript import EventQueue, EventType

POINTS = {
    "minecraft:cod": 1,
    "minecraft:salmon": 2,
    "minecraft:pufferfish": 2,
    "minecraft:tropical_fish": 4,
    "minecraft:name_tag": 4,
    "minecraft:nautilus_shell": 4,
    "minecraft:enchanted_book": 6,
    "minecraft:saddle": 6,
    "minecraft:bow": 6,
    "minecraft:potion": 6,
    "minecraft:leather": 6,
    "minecraft:lily_pad": 6,
    "minecraft:rotten_flesh": 6,
    "minecraft:tripwire_hook": 6,
    "minecraft:stick": 6,
    "minecraft:string": 8,
    "minecraft:bowl": 6,
    "minecraft:leather_boots": 6,
    "minecraft:bone": 6,
    "minecraft:fishing_rod": 10,
    "minecraft:ink_sac": 10,
}

SCOREBOARD = "fishing_score"
BOSSBAR = "fishing_timer"

home_pos = None
lake_pos = None
game_duration = 180  # 秒
game_running = False
game_thread = None

def title_subtitle(title, subtitle=None, title_color="gold", subtitle_color="white"):
    m.execute("title @a clear")
    m.execute(f'title @a title {{"text":"{title}","color":"{title_color}","bold":true}}')
    if subtitle:
        m.execute(f'title @a subtitle {{"text":"{subtitle}","color":"{subtitle_color}"}}')

def bossbar_set(name, progress):
    # ボスバーが無ければ追加＆表示設定
    m.execute(f"bossbar add {BOSSBAR} \"Fishing Timer\"")
    m.execute(f"bossbar set {BOSSBAR} players @a")
    m.execute(f"bossbar set {BOSSBAR} max {game_duration}")
    # 値と名前をセット
    value = max(0, min(int(progress * game_duration), game_duration))
    m.execute(f"bossbar set {BOSSBAR} value {value}")
    m.execute(f"bossbar set {BOSSBAR} name \"{name}\"")

def bossbar_clear():
    m.execute(f"bossbar remove {BOSSBAR}")

def snapshot_inventory():
    return {item.item: item.count for item in m.player_inventory() if item.count > 0}

def tell(msg, color="white"):
    m.execute(f'tellraw @a {{"text":"{msg}","color":"{color}"}}')

def reset_game():
    global game_running
    game_running = False
    m.execute(f"scoreboard players reset @p {SCOREBOARD}")
    bossbar_clear()
    tell("Game reset.", "gray")

def teleport(pos):
    if pos:
        x, y, z = pos
        m.execute(f"tp @p {x} {y} {z}")
    else:
        tell("Teleport location not set.", "red")

def start_game():
    global game_running, game_thread

    if not lake_pos:
        tell("Lake location not set. Use --setlake", "red")
        return

    teleport(lake_pos)

    # スコアボード作成（なければ追加）
    m.execute(f"scoreboard objectives add {SCOREBOARD} dummy FishingScore")
    m.execute(f"scoreboard players set @p {SCOREBOARD} 0")

    m.execute('/item replace entity @p hotbar.0 with minecraft:fishing_rod')
    for ench in ["luck_of_the_sea 3", "lure 3", "unbreaking 3", "mending 1"]:
        m.execute(f"/enchant @p {ench}")

    tell(f"Fishing Game Started! ({game_duration} seconds)", "yellow")
    game_running = True

    def run_game():
        score = 0
        prev_inv = snapshot_inventory()
        start = time.time()

        while game_running:
            elapsed = time.time() - start
            if elapsed >= game_duration:
                break

            remaining = game_duration - elapsed
            bossbar_set(f"Time Left: {int(remaining)}s", remaining / game_duration)

            current_inv = snapshot_inventory()
            for item_id in current_inv:
                if item_id in POINTS:
                    prev_count = prev_inv.get(item_id, 0)
                    curr_count = current_inv[item_id]
                    if curr_count > prev_count:
                        delta = curr_count - prev_count
                        gained = delta * POINTS[item_id]
                        score += gained
                        m.execute(f"scoreboard players set @p {SCOREBOARD} {score}")
                        tell(f"+{gained} pts for {item_id.split(':')[1]}", "aqua")
            prev_inv = current_inv
            time.sleep(0.25)

        bossbar_clear()
        title_subtitle("Time's up!", f"Score: {score}", "gold", "green")
        if home_pos:
            teleport(home_pos)

    game_thread = threading.Thread(target=run_game)
    game_thread.start()

def stop_game():
    global game_running
    game_running = False
    bossbar_clear()
    tell("Game forcibly stopped.", "red")
    if home_pos:
        teleport(home_pos)

# メインのチャットイベント処理
def main():
    global home_pos, lake_pos, game_duration

    with EventQueue() as q:
        q.register_chat_listener()
        tell("Fishing Game Controller ready.", "green")
        while True:
            event = q.get()
            if event.type != EventType.CHAT:
                continue
            msg = event.message.strip()

            if msg.startswith("<") and ">" in msg:
                msg = msg.split(">", 1)[1].strip()

            if not msg.startswith("--"):
                continue

            if msg == "--sethome":
                home_pos = tuple(int(c) for c in m.player_position())
                tell(f"Home set to {home_pos}", "yellow")

            elif msg == "--setlake":
                lake_pos = tuple(int(c) for c in m.player_position())
                tell(f"Lake set to {lake_pos}", "blue")

            elif msg.startswith("--settime"):
                parts = msg.split()
                if len(parts) == 2 and parts[1].isdigit():
                    game_duration = int(parts[1])
                    tell(f"Game time set to {game_duration} seconds.", "yellow")
                else:
                    tell("Invalid format. Use --settime <seconds>", "red")

            elif msg == "--start":
                if game_running:
                    tell("Game already running.", "red")
                else:
                    start_game()

            elif msg == "--stop":
                stop_game()

            elif msg == "--reset":
                reset_game()

if __name__ == "__main__":
    main()
