import minescript as m
import time
import threading
from minescript import EventQueue, EventType, echo

'''
JE 1.20.1 / Minescript 4.0
'''

# =========================
# 状態フラグ
# =========================
_fishing_active = False
_stop_flag = False

# =========================
# 釣り関数
# =========================
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
            # 浮きが動いた（魚がかかった）判定
            if y - last_y > 0.2:
                return True
            last_y = y
        time.sleep(0.1)
    return False

def auto_fish_loop():
    global _stop_flag, _fishing_active
    # echo("🎣 自動釣り開始！")
    while not _stop_flag:
        # 投げる
        m.player_press_use(True)
        m.player_press_use(False)
        time.sleep(2)

        bobber = find_bobber()
        if bobber and wait_for_bite(bobber):
            # 釣る
            m.player_press_use(True)
            m.player_press_use(False)

        time.sleep(1)
    _fishing_active = False
    # echo("🛑 自動釣り停止")

# =========================
# GキーでON/OFFトグル
# =========================
def toggle_fishing():
    global _fishing_active, _stop_flag
    if not _fishing_active:
        _fishing_active = True
        _stop_flag = False
        threading.Thread(target=auto_fish_loop, daemon=True).start()
    else:
        _stop_flag = True
        _fishing_active = False

# =========================
# イベントループ
# =========================
def main():
    # echo("🎣 Gキーで釣りの自動ON/OFFを切り替えます")
    with EventQueue() as q:
        q.register_key_listener()
        while True:
            event = q.get()
            if event.type == EventType.KEY and event.action == 0:  # key up
                if event.key == 71:  # Gキー
                    toggle_fishing()
            time.sleep(0.01)

if __name__ == "__main__":
    main()
