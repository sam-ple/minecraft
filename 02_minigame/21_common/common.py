# ==============================
# common.py
# ミニゲーム共通ユーティリティ
# ==============================

import minescript as m
import json, math, time, os

# ==============================
# UI
# ==============================
def chat(msg, color="white"):
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": color})}')

def title_main(text, color="gold"):
    m.execute(f'title @a title {json.dumps({"text": text, "bold": True, "color": color})}')

def title_sub(text, color="yellow"):
    m.execute(f'title @a subtitle {json.dumps({"text": text, "color": color})}')

def sound_pling():
    m.execute("playsound minecraft:block.note_block.pling master @a")

def sec_to_mmss(sec):
    m_, s_ = divmod(max(int(sec), 0), 60)
    return f"{m_:02d}:{s_:02d}"

# ==============================
# カウントダウン
# ==============================
def countdown_start():
    for i in [3, 2, 1]:
        title_main(str(i), "red")
        sound_pling()
        time.sleep(1)
    title_main("GAME START")
    sound_pling()
    time.sleep(0.5)

def countdown_end(seconds=10):
    for i in range(seconds, 0, -1):
        title_main(str(i), "red")
        sound_pling()
        time.sleep(1)
    title_main("GAME END")
    sound_pling()
    time.sleep(0.5)

# ==============================
# 開始地点管理
# ==============================
def save_start_pos(path):
    x, y, z = m.player_position()
    pos = {
        "x": math.floor(x),
        "y": math.floor(y),
        "z": math.floor(z)
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pos, f, indent=2)

def load_start_pos(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def tp_all_to_start(path):
    pos = load_start_pos(path)
    if pos:
        m.execute(f"tp @a {pos['x']} {pos['y']} {pos['z']}")

# ==============================
# bossbar
# ==============================
def setup_bossbar(bar_id, title, duration):
    m.execute(f"bossbar remove {bar_id}")
    m.execute(f'bossbar add {bar_id} {json.dumps({"text": title, "color": "gold"})}')
    m.execute(f"bossbar set {bar_id} max {duration}")
    m.execute(f"bossbar set {bar_id} value {duration}")
    m.execute(f"bossbar set {bar_id} players @a")

def update_bossbar(bar_id, start_time, duration):
    remain = max(duration - int(time.time() - start_time), 0)
    m.execute(f"bossbar set {bar_id} value {remain}")
    m.execute(f'bossbar set {bar_id} name "{sec_to_mmss(remain)}"')
    return remain

def remove_bossbar(bar_id):
    m.execute(f"bossbar remove {bar_id}")

# ==============================
# scoreboard
# ==============================
def reset_scoreboard(obj):
    m.execute(f"scoreboard objectives remove {obj}")

def create_scoreboard(obj, title):
    m.execute(f'scoreboard objectives add {obj} dummy "{title}"')
    m.execute(f"scoreboard objectives setdisplay sidebar {obj}")

# ==============================
# ゲーム共通終了処理
# ==============================
def end_game_common(bar_id, start_pos_file):
    remove_bossbar(bar_id)
    tp_all_to_start(start_pos_file)
