import minescript as m
import time
import random
from threading import Thread
from minescript_plus import Keybind

_fishing_active = False  # 釣り中かどうか
_stop_flag = False       # 停止用フラグ

# =========================
# ボッバー(ウキ)検出
# =========================
def find_bobber():
    for e in m.entities():
        if "fishing_bobber" in e.type.lower():
            return e
    return None

# =========================
# 魚がかかるまで待機
# =========================
def wait_for_bite(bobber, timeout=30):
    start = time.time()
    last_y = bobber.position[1]
    while time.time() - start < timeout:
        if _stop_flag:
            return False
        entity = find_bobber()
        if entity:
            y = entity.position[1]
            if y - last_y > 0.2:  # ウキが浮き上がる＝魚がかかった
                return True
            last_y = y
        time.sleep(0.1)
    return False

# =========================
# 自動釣りループ
# =========================
def auto_fish_loop():
    global _stop_flag, _fishing_active
    print("🎣 Auto fishing started.")
    
    # AFK防止スレッド開始
    Thread(target=afk_prevention_loop, daemon=True).start()

    while not _stop_flag:
        # 投げる
        m.player_press_use(True)
        m.player_press_use(False)
        time.sleep(2)

        bobber = find_bobber()
        if bobber and wait_for_bite(bobber):
            # 魚を引き上げ
            m.player_press_use(True)
            m.player_press_use(False)
            print("🐟 Fish caught!")

        time.sleep(1)

    print("🛑 Auto fishing stopped.")
    _fishing_active = False

# =========================
# AFK防止ループ
# =========================
def afk_prevention_loop():
    """3〜5分ごとにスニークまたはジャンプ"""
    while not _stop_flag:
        wait_time = random.uniform(180, 300)  # 3〜5分
        time.sleep(wait_time)
        if _stop_flag:
            break

        action = random.choice(["sneak", "jump"])
        if action == "sneak":
            print("💤 AFK防止: スニーク中...")
            m.player_press_sneak(True)
            time.sleep(random.uniform(1.0, 2.0))
            m.player_press_sneak(False)
        else:
            print("💤 AFK防止: ジャンプ！")
            m.player_press_jump(True)
            time.sleep(0.2)
            m.player_press_jump(False)

# =========================
# トグル関数（GキーでON/OFF）
# =========================
def toggle_fishing():
    global _fishing_active, _stop_flag
    if not _fishing_active:
        _fishing_active = True
        _stop_flag = False
        Thread(target=auto_fish_loop, daemon=True).start()
    else:
        _stop_flag = True
        _fishing_active = False

# =========================
# Keybind登録
# =========================
kb = Keybind()
kb.set_keybind(71, toggle_fishing)  # Gキー

# =========================
# メインループ
# =========================
while True:
    time.sleep(1)
