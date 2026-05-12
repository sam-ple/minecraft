import minescript as m
import time
from minescript_plus import Keybind

_fishing_active = False  # 釣り中かどうか
_stop_flag = False       # 停止用フラグ

def find_bobber():
    for e in m.entities():
        if "fishing_bobber" in e.type.lower():
            return e
    return None

def wait_for_bite(bobber, timeout=30):
    start = time.time()
    last_y = bobber.position[1]
    while time.time() - start < timeout:
        if _stop_flag:
            return False
        entity = find_bobber()
        if entity:
            y = entity.position[1]
            if y - last_y > 0.2:
                return True
            last_y = y
        time.sleep(0.1)
    return False

def toggle_fishing():
    """Gキー押下で釣り開始 / 停止切り替え"""
    global _fishing_active, _stop_flag
    if not _fishing_active:
        _fishing_active = True
        _stop_flag = False
        m.press_key_bind("key.use", True)   # 投げる用に保持開始
        # 釣りループを別スレッドで実行してブロックしないようにする
        from threading import Thread
        Thread(target=auto_fish_loop, daemon=True).start()
    else:
        _stop_flag = True
        _fishing_active = False

def auto_fish_loop():
    global _stop_flag, _fishing_active
    while not _stop_flag:
        # 竿を投げる
        m.player_press_use(True)
        m.player_press_use(False)
        time.sleep(2)

        bobber = find_bobber()
        if bobber and wait_for_bite(bobber):
            # 魚を釣る
            m.player_press_use(True)
            m.player_press_use(False)

        time.sleep(1)
    _fishing_active = False

# =========================
# Keybind登録
# =========================
kb = Keybind()
kb.set_keybind(71, toggle_fishing)  # Gキー

# 無限ループでKeybindを維持
while True:
    time.sleep(1)
