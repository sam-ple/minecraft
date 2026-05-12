# Trying Out Minescript on Multiple Servers

<!-- Tiny Extras 1/2/3 -->

This section records my test scripts and ongoing experiments in a multiserver environment. 
I gradually refine each tool (HUD, chat logger, autofishing, advancement tracker, etc.) 
by adding features, debugging behavior, and verifying how they work across different servers.

## 2025/10/29

Initial setup and early tests. Added basic chat logging, a minimal HUD,
and the first version of the autofishing script. Focus was on confirming
event listeners and simple HUD updates.

### run.py

```python
import minescript as m

m.execute("\\chatlog")
m.execute("\\hud")
m.execute("\\fish")
```

### chatlog_v0.0.01_20250922.py

```python
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
```

### microhud_v0.0.00_orig.py

- @razrcraft
- https://discord.com/channels/930220988472389713/1414377991395610646/1414377991395610646

```python
import math
from time import sleep
from minescript import player_position, echo
from java import JavaClass
from minescript_plus import Hud

Minecraft = JavaClass("net.minecraft.client.Minecraft")

mc = Minecraft.getInstance()

# Placeholders
t_pos = Hud.add_text("Pos: ", 5, 5)
t_fps = Hud.add_text("FPS: ", 5, 20)

Hud.use_toggle_key(True)
echo("MicroHUD started. Use F12 to toggle.")

while True:
    x, y, z = [f"{p:.2f}" for p in player_position()]
    fps = mc.getFps()
    Hud.set_text_string(t_pos, f"Pos: {x}, {y}, {z}")
    Hud.set_text_string(t_fps, f"FPS: {fps}")
    sleep(.1)
```

### autofish_v0.0.01_20251029.py

```python
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
```

## 2025/10/30

Expanded the HUD with biome, direction, ping, and input tracking.
Started experimenting with key and mouse event listeners.
Overall aim was to build a more informative on-screen overlay.


### microhud_v0.0.04_20251030.py

```python
from time import sleep
from datetime import datetime
from minescript import player_position, player_orientation, echo, EventQueue, EventType
from java import JavaClass
from minescript_plus import Hud, Server
import threading

# === Minecraft hooks ===
Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance()

# === GLFW Key Names ===
GLFW_KEY_NAMES = {
    32: "SPACE", 39: "'", 44: ",", 45: "-", 46: ".", 47: "/",
    48: "0", 49: "1", 50: "2", 51: "3", 52: "4", 53: "5", 54: "6", 55: "7", 56: "8", 57: "9",
    59: ";", 61: "=", 65: "A", 66: "B", 67: "C", 68: "D", 69: "E", 70: "F",
    71: "G", 72: "H", 73: "I", 74: "J", 75: "K", 76: "L", 77: "M",
    78: "N", 79: "O", 80: "P", 81: "Q", 82: "R", 83: "S", 84: "T",
    85: "U", 86: "V", 87: "W", 88: "X", 89: "Y", 90: "Z",
    91: "[", 92: "\\", 93: "]", 96: "`",
    257: "ENTER", 258: "TAB", 259: "BACKSPACE", 260: "INSERT", 261: "DELETE",
    262: "RIGHT", 263: "LEFT", 264: "DOWN", 265: "UP",
    266: "PAGE_UP", 267: "PAGE_DOWN", 268: "HOME", 269: "END",
    280: "CAPS_LOCK", 281: "SCROLL_LOCK", 282: "NUM_LOCK",
    283: "PRINT_SCREEN", 284: "PAUSE",
    290: "F1", 291: "F2", 292: "F3", 293: "F4", 294: "F5", 295: "F6",
    296: "F7", 297: "F8", 298: "F9", 299: "F10", 300: "F11", 301: "F12",
    320: "NUMPAD_0", 321: "NUMPAD_1", 322: "NUMPAD_2", 323: "NUMPAD_3",
    324: "NUMPAD_4", 325: "NUMPAD_5", 326: "NUMPAD_6", 327: "NUMPAD_7",
    328: "NUMPAD_8", 329: "NUMPAD_9",
    330: "NUMPAD_DOT", 331: "NUMPAD_DIVIDE", 332: "NUMPAD_MULTIPLY",
    333: "NUMPAD_MINUS", 334: "NUMPAD_PLUS", 335: "NUMPAD_ENTER",
    336: "NUMPAD_EQUAL",
    340: "L_SHIFT", 341: "L_CTRL", 342: "L_ALT", 343: "L_SUPER",
    344: "R_SHIFT", 345: "R_CTRL", 346: "R_ALT", 347: "R_SUPER",
    348: "MENU", 256: "ESCAPE",
}

MOUSE_NAMES = {0: "LMB", 1: "RMB", 2: "MMB"}

def get_key_name(key_code: int) -> str:
    return GLFW_KEY_NAMES.get(key_code, f"K{key_code}")

def get_mouse_name(button: int) -> str:
    return MOUSE_NAMES.get(button, f"M{button}")

# === HUD elements ===
t_pos  = Hud.add_text("Pos: ", 5, 5)
t_fps  = Hud.add_text("FPS: ", 5, 20)
t_bio  = Hud.add_text("Biome: ", 5, 35)
t_dir  = Hud.add_text("Dir: ", 5, 50)
t_time = Hud.add_text("Time: ", 5, 65)
t_ping = Hud.add_text("Ping: ", 5, 80)
t_inp  = Hud.add_text("Input: ", 5, 95)

Hud.use_toggle_key(True)
print("MicroHUD+ started. (toggle: F12)")

# === Direction helper ===
def yaw_to_direction(yaw: float) -> str:
    yaw = (yaw % 360 + 360) % 360
    if 45 <= yaw < 135:
        return "West"
    elif 135 <= yaw < 225:
        return "North"
    elif 225 <= yaw < 315:
        return "East"
    else:
        return "South"

# === Biome getter ===
def get_biome_name():
    if mc.level is None or mc.player is None:
        return "Unknown"
    try:
        player_pos = mc.player.blockPosition()
        biome_holder = mc.level.getBiome(player_pos)
        biome_key = biome_holder.unwrapKey().get()
        return biome_key.location().toString().replace("minecraft:", "")
    except Exception:
        return "Unknown"

# === Input tracking ===
keys_pressed = set()
mouse_pressed = set()

eq = EventQueue()
eq.register_key_listener()
eq.register_mouse_listener()

def process_input_events():
    while True:
        e = eq.get()
        if e.type == EventType.KEY:
            if e.action == 1:
                keys_pressed.add(e.key)
            elif e.action == 0:
                keys_pressed.discard(e.key)
        elif e.type == EventType.MOUSE:
            if e.action == 1:
                mouse_pressed.add(e.button)
            elif e.action == 0:
                mouse_pressed.discard(e.button)
        sleep(0.01)

threading.Thread(target=process_input_events, daemon=True).start()

# === Main loop ===
while True:
    try:
        x, y, z = [f"{p:.2f}" for p in player_position()]
        fps = mc.getFps()
        biome = get_biome_name()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ping = Server.get_ping()
        yaw, pitch = player_orientation()
        direction = yaw_to_direction(yaw)

        key_names = [get_key_name(k) for k in keys_pressed]
        mouse_names = [get_mouse_name(b) for b in mouse_pressed]
        input_text = f"Keys: {', '.join(key_names) if key_names else 'None'} | Mouse: {', '.join(mouse_names) if mouse_names else 'None'}"

        Hud.set_text_string(t_pos,  f"Pos: {x}, {y}, {z}")
        Hud.set_text_string(t_fps,  f"FPS: {fps}")
        Hud.set_text_string(t_bio,  f"Biome: {biome}")
        Hud.set_text_string(t_dir,  f"Dir: {direction} ({int(yaw)}°, {int(pitch)}°)")
        Hud.set_text_string(t_time, f"Time: {now}")
        Hud.set_text_string(t_ping, f"Ping: {ping if ping is not None else 'N/A'} ms")
        Hud.set_text_string(t_inp,  input_text)

        sleep(0.1)
    except Exception as e:
        print(f"HUD Error: {e}")
        sleep(1)
```

## 2025/11/01

Introduced additional utility scripts including advancement tracking,
damage event debugging, and inventory steal/dump automation.
HUD received further refinement and more data sources.


### run.py

```python
import minescript as m

m.execute("\\chatlog")
m.execute("\\hud")
m.execute("\\fish")
m.execute("\\adv")
m.execute("\\damage")
m.execute("\\steal_dump")
```

### microhud_v0.0.05_20251031.py

```python
from time import sleep
from datetime import datetime
import threading
from minescript import (
    player_position, player_orientation, echo,
    player_get_targeted_block, player_get_targeted_entity,
    version_info, EventQueue, EventType
)
from java import JavaClass
from minescript_plus import Hud, Server

# === Minecraft hooks ===
Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance()

# === GLFW Key Names ===
GLFW_KEY_NAMES = {
    32: "SPACE", 39: "'", 44: ",", 45: "-", 46: ".", 47: "/",
    48: "0", 49: "1", 50: "2", 51: "3", 52: "4", 53: "5", 54: "6", 55: "7", 56: "8", 57: "9",
    59: ";", 61: "=", 65: "A", 66: "B", 67: "C", 68: "D", 69: "E", 70: "F",
    71: "G", 72: "H", 73: "I", 74: "J", 75: "K", 76: "L", 77: "M",
    78: "N", 79: "O", 80: "P", 81: "Q", 82: "R", 83: "S", 84: "T",
    85: "U", 86: "V", 87: "W", 88: "X", 89: "Y", 90: "Z",
    91: "[", 92: "\\", 93: "]", 96: "`",
    257: "ENTER", 258: "TAB", 259: "BACKSPACE", 260: "INSERT", 261: "DELETE",
    262: "RIGHT", 263: "LEFT", 264: "DOWN", 265: "UP",
    266: "PAGE_UP", 267: "PAGE_DOWN", 268: "HOME", 269: "END",
    280: "CAPS_LOCK", 281: "SCROLL_LOCK", 282: "NUM_LOCK",
    283: "PRINT_SCREEN", 284: "PAUSE",
    290: "F1", 291: "F2", 292: "F3", 293: "F4", 294: "F5", 295: "F6",
    296: "F7", 297: "F8", 298: "F9", 299: "F10", 300: "F11", 301: "F12",
    320: "NUMPAD_0", 321: "NUMPAD_1", 322: "NUMPAD_2", 323: "NUMPAD_3",
    324: "NUMPAD_4", 325: "NUMPAD_5", 326: "NUMPAD_6", 327: "NUMPAD_7",
    328: "NUMPAD_8", 329: "NUMPAD_9",
    330: "NUMPAD_DOT", 331: "NUMPAD_DIVIDE", 332: "NUMPAD_MULTIPLY",
    333: "NUMPAD_MINUS", 334: "NUMPAD_PLUS", 335: "NUMPAD_ENTER",
    336: "NUMPAD_EQUAL",
    340: "L_SHIFT", 341: "L_CTRL", 342: "L_ALT", 343: "L_SUPER",
    344: "R_SHIFT", 345: "R_CTRL", 346: "R_ALT", 347: "R_SUPER",
    348: "MENU", 256: "ESCAPE",
}
MOUSE_NAMES = {0: "LMB", 1: "RMB", 2: "MMB"}

def get_key_name(key_code: int) -> str:
    return GLFW_KEY_NAMES.get(key_code, f"K{key_code}")

def get_mouse_name(button: int) -> str:
    return MOUSE_NAMES.get(button, f"M{button}")

# === HUD elements ===
y = 5
line_h = 15
def next_line():
    global y
    y += line_h
    return y

t_ver  = Hud.add_text("", 5, next_line())
t_pos  = Hud.add_text("", 5, next_line())
t_fps  = Hud.add_text("", 5, next_line())
t_bio  = Hud.add_text("", 5, next_line())
t_dir  = Hud.add_text("", 5, next_line())
t_time = Hud.add_text("", 5, next_line())
t_ping = Hud.add_text("", 5, next_line())
t_mob  = Hud.add_text("", 5, next_line())
t_blk  = Hud.add_text("", 5, next_line())
t_inp  = Hud.add_text("", 5, next_line())

Hud.use_toggle_key(True)
print("MicroHUD+ started. (toggle: F12)")

# === Direction helper ===
def yaw_to_direction(yaw: float) -> str:
    yaw = ((yaw + 180) % 360) - 180  # normalize
    dirs = [
        "South", "South-West", "West", "North-West",
        "North", "North-East", "East", "South-East"
    ]
    index = int(((yaw + 180) / 45) + 0.5) % 8
    return dirs[index]

# === Biome getter ===
def get_biome_name():
    if mc.level is None or mc.player is None:
        return "Unknown"
    try:
        player_pos = mc.player.blockPosition()
        biome_holder = mc.level.getBiome(player_pos)
        biome_key = biome_holder.unwrapKey().get()
        return biome_key.location().toString().replace("minecraft:", "")
    except Exception:
        return "Unknown"

# === Input tracking ===
keys_pressed = set()
mouse_pressed = set()

eq = EventQueue()
eq.register_key_listener()
eq.register_mouse_listener()

def process_input_events():
    while True:
        e = eq.get()
        if e.type == EventType.KEY:
            if e.action == 1:
                keys_pressed.add(e.key)
            elif e.action == 0:
                keys_pressed.discard(e.key)
        elif e.type == EventType.MOUSE:
            if e.action == 1:
                mouse_pressed.add(e.button)
            elif e.action == 0:
                mouse_pressed.discard(e.button)
        sleep(0.01)

threading.Thread(target=process_input_events, daemon=True).start()

# === Main loop ===
while True:
    try:
        # === Version Info ===
        v = version_info()
        ver_text = f"VersionInfo : MC {v.minecraft} / MS {v.minescript} / {v.mod_loader} / {v.pyjinn}"

        # === Player Info ===
        x, y, z = [f"{p:.2f}" for p in player_position()]
        fps = mc.getFps()
        biome = get_biome_name()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ping = Server.get_ping()
        yaw, pitch = player_orientation()
        yaw = ((yaw + 180) % 360) - 180
        pitch = ((pitch + 180) % 360) - 180
        direction = yaw_to_direction(yaw)

        # === Entity & Block ===
        e = player_get_targeted_entity(20)
        mob_text = f"Mob: {e.type}" if e else "Mob: none"
        b = player_get_targeted_block(20)
        blk_text = f"Block: {b.type.replace('minecraft:', '')}" if b else "Block: none"

        # === Input ===
        key_names = [get_key_name(k) for k in keys_pressed]
        mouse_names = [get_mouse_name(b) for b in mouse_pressed]
        input_text = f"Keys: {', '.join(key_names) if key_names else 'None'} | Mouse: {', '.join(mouse_names) if mouse_names else 'None'}"

        # === Update HUD ===
        Hud.set_text_string(t_ver,  ver_text)
        Hud.set_text_string(t_pos,  f"Pos: {x}, {y}, {z}")
        Hud.set_text_string(t_fps,  f"FPS: {fps}")
        Hud.set_text_string(t_bio,  f"Biome: {biome}")
        Hud.set_text_string(t_dir,  f"Dir: {direction} ({int(yaw)}°, {int(pitch)}°)")
        Hud.set_text_string(t_time, f"Time: {now}")
        Hud.set_text_string(t_ping, f"Ping: {ping if ping is not None else 'N/A'} ms")
        Hud.set_text_string(t_mob,  mob_text)
        Hud.set_text_string(t_blk,  blk_text)
        Hud.set_text_string(t_inp,  input_text)

        sleep(0.1)

    except Exception as e:
        print(f"HUD Error: {e}")
        sleep(1)
```

### fish_v0.0.02_20251031.py

```python
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
# Randomly perform a small action to prevent AFK kick
# (Server anti-AFK systems usually detect total inactivity)
def afk_prevention_loop():
    """3〜5分ごとにスニークまたはジャンプ"""
    while not _stop_flag:
        wait_time = random.uniform(180, 300)  # 3〜5分
        time.sleep(wait_time)
        if _stop_flag:
            break

        action = random.choice(["sneak", "jump"])
        if action == "sneak":
            # print("AFK Prevention: Sneaking...")
            m.player_press_sneak(True)
            time.sleep(random.uniform(1.0, 2.0)) # Hold sneak for 1–2 seconds
            m.player_press_sneak(False)
        else:
            # print("💤 AFK防止: ジャンプ！")
            print("AFK Prevention: Jumping!")
            m.player_press_jump(True)
            time.sleep(0.2) # Short jump press
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
```

### adv0_v0.0.02_20251031.py

```python
import minescript as m
from minescript import EventQueue, EventType
import re
import json
import os

# 保存ファイル（同フォルダ内）
SAVE_FILE = "advancement_records.json"

# チャットの進捗メッセージを検出
adv_pattern = re.compile(r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]")

eq = EventQueue()
eq.register_chat_listener()

# データ読み込み
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)
else:
    records = {}

# 初達成チェック
first_adv = set(
    adv for player in records.values() for adv in player.get("advancements", [])
)

m.echo("📘 Advancement Tracker+ (self-only) started!")
m.echo(f"Loaded {len(records)} player records from {SAVE_FILE}")

def save_records():
    """ファイル保存"""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

while True:
    event = eq.get()
    if not event or event.type != EventType.CHAT:
        continue

    msg = event.message.strip()
    match = adv_pattern.match(msg)
    if not match:
        continue

    player, action, adv_name = match.groups()
    add_point = 1

    # データ初期化
    if player not in records:
        records[player] = {"points": 0, "advancements": []}

    # 初達成ボーナス
    if adv_name not in first_adv:
        first_adv.add(adv_name)
        add_point += 1
        m.echo(f"✨ {player} got FIRST for '{adv_name}' (+1 bonus)")

    # 重複取得はスキップ
    if adv_name not in records[player]["advancements"]:
        records[player]["advancements"].append(adv_name)
        records[player]["points"] += add_point
        save_records()

        m.echo(f"📈 {player}: +{add_point}pt (Total {records[player]['points']}) [{adv_name}]")
    else:
        m.echo(f"ℹ️ {player} already had '{adv_name}', skipped.")
```

### damageevent_v0.1.00_20251007.py

```python
import minescript as m
from minescript import EventQueue, EventType
import math

eq = EventQueue()
eq.register_damage_listener()

m.echo("⚡ DamageEvent debug mode: waiting for damage...")

def resolve_entity(uuid):
    """UUIDからEntityDataを返す（Player優先）"""
    if not uuid:
        return None
    
    players_list = m.players(uuid=uuid)
    if players_list:
        return players_list[0]
    
    entities_list = m.entities(uuid=uuid)
    if entities_list:
        return entities_list[0]
    
    return None


def format_name(ent):
    """名前＋種別"""
    if ent is None:
        return "Unknown", "?"
    
    if getattr(ent, "local", False):
        return ent.name, "Player"
    elif "minecraft:" in getattr(ent, "type", ""):
        return ent.type.split(":")[-1].replace("_", " ").title(), "Mob"
    else:
        return getattr(ent, "name", None) or getattr(ent, "type", "?"), "Entity"


def get_xyz(pos):
    """posがlist/tupleまたはオブジェクトのどちらでも(x, y, z)を返す"""
    if pos is None:
        return None
    if isinstance(pos, (list, tuple)) and len(pos) >= 3:
        return pos[0], pos[1], pos[2]
    if all(hasattr(pos, k) for k in ("x", "y", "z")):
        return pos.x, pos.y, pos.z
    return None


def distance(pos1, pos2):
    """距離を計算"""
    a = get_xyz(pos1)
    b = get_xyz(pos2)
    if not a or not b:
        return None
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)


COLOR = {
    "Player": "§9",
    "Mob": "§c",
    "Entity": "§d",
    "Source": "§e",
    "Reset": "§r"
}

# 自然ダメージ系のソース一覧
ENVIRONMENTAL_SOURCES = {
    "fall", "drown", "lava", "fire", "cactus", "lightning", "starve",
    "suffocate", "explosion", "cramming", "freeze", "sweet_berry_bush", "magic"
}


while True:
    event = eq.get()
    if not event or event.type != EventType.DAMAGE:
        continue

    victim = resolve_entity(event.entity_uuid)
    attacker = resolve_entity(event.cause_uuid)

    victim_name, victim_type = format_name(victim)
    attacker_name, attacker_type = format_name(attacker)

    dist = distance(
        getattr(victim, "position", None),
        getattr(attacker, "position", None)
    )

    source = event.source.lower() if event.source else "unknown"
    source_text = f"{COLOR['Source']}{source}{COLOR['Reset']}"

    # 出力文（自然ダメージは矢印なし）
    if source in ENVIRONMENTAL_SOURCES or attacker_name == "Unknown":
        msg = f"💥 {COLOR.get(victim_type,'')}{victim_name}{COLOR['Reset']} took {source_text} damage"
    else:
        msg = (
            f"💥 {COLOR.get(attacker_type,'')}{attacker_name}{COLOR['Reset']} "
            f"---> {COLOR.get(victim_type,'')}{victim_name}{COLOR['Reset']} "
            f"[{source_text}]"
        )

    if dist is not None and source not in ENVIRONMENTAL_SOURCES:
        msg += f" 📏{round(dist,1)}m"

    if victim and getattr(victim, "health", None) is not None:
        msg += f" ❤️{round(victim.health,1)}HP"

    m.echo(msg)
```

### steal_dump_v0.0.00_orig.pyj

- @razrcraft
- https://discord.com/channels/930220988472389713/1068545062646059128/threads/1415120855301754880

```python
Minecraft = JavaClass("net.minecraft.client.Minecraft")
ScreenEvents = JavaClass("net.fabricmc.fabric.api.client.screen.v1.ScreenEvents")
ScreenEventsAfterInit = JavaClass("net.fabricmc.fabric.api.client.screen.v1.ScreenEvents$AfterInit")
Screens = JavaClass("net.fabricmc.fabric.api.client.screen.v1.Screens")
Button = JavaClass("net.minecraft.client.gui.components.Button")
Component = JavaClass("net.minecraft.network.chat.Component") 
ContainerScreen = JavaClass("net.minecraft.client.gui.screens.inventory.ContainerScreen")
ShulkerBoxScreen = JavaClass("net.minecraft.client.gui.screens.inventory.ShulkerBoxScreen")
ClickType = JavaClass("net.minecraft.world.inventory.ClickType")

mc = Minecraft.getInstance()

def move_items(dump: bool=False):
    container_menu = mc.screen.getMenu()
    size = container_menu.getItems().size() - 36
        
    if dump:
        start = size
        end = size + 36
    else:
        start = 0
        end = size
        
    for slot in range(start, end):
        if not container_menu.getSlot(slot).hasItem():
            continue

        mc.gameMode.handleInventoryMouseClick(
            container_menu.containerId, slot, 0, ClickType.QUICK_MOVE, mc.player)

def steal_button(button):
    move_items()

def dump_button(button):
    move_items(True)

def after_init(client, screen, scaledWidth, scaledHeight):
    if type(screen) is ContainerScreen or type(screen) is ShulkerBoxScreen:
        container_menu = mc.screen.getMenu()
        size = container_menu.getItems().size() - 36
        x = int(scaledWidth / 2)
        y = int(scaledHeight / 2) - 90
        if size == 54:
            y -= 27
        
        Screens.getButtons(screen).add(Button.Builder(Component.literal("Steal"), steal_button).pos(x, y).size(40, 20).build())
        Screens.getButtons(screen).add(Button.Builder(Component.literal("Dump"), dump_button).pos(x + 42, y).size(40, 20).build())

afterinit_callback = ManagedCallback(after_init) 
ScreenEvents.AFTER_INIT.register(ScreenEventsAfterInit(afterinit_callback))
```

## 2025/11/04

Enhanced the HUD again with hand item display and refined direction logic.
Focused on stability, readability, and capturing more player state details.


### microhud_v0.0.07_20251104.py

```python
from time import sleep
from datetime import datetime
import threading
import minescript as m
from minescript import (
    player_position, player_orientation, echo,
    player_get_targeted_block, player_get_targeted_entity,
    version_info, EventQueue, EventType, player_hand_items
)
from java import JavaClass
from minescript_plus import Hud, Server

# === Minecraft hooks ===
Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance()

# === GLFW Key Names ===
GLFW_KEY_NAMES = {
    32: "SPACE", 39: "'", 44: ",", 45: "-", 46: ".", 47: "/",
    48: "0", 49: "1", 50: "2", 51: "3", 52: "4", 53: "5", 54: "6", 55: "7", 56: "8", 57: "9",
    59: ";", 61: "=", 65: "A", 66: "B", 67: "C", 68: "D", 69: "E", 70: "F",
    71: "G", 72: "H", 73: "I", 74: "J", 75: "K", 76: "L", 77: "M",
    78: "N", 79: "O", 80: "P", 81: "Q", 82: "R", 83: "S", 84: "T",
    85: "U", 86: "V", 87: "W", 88: "X", 89: "Y", 90: "Z",
    91: "[", 92: "\\", 93: "]", 96: "`",
    257: "ENTER", 258: "TAB", 259: "BACKSPACE", 260: "INSERT", 261: "DELETE",
    262: "RIGHT", 263: "LEFT", 264: "DOWN", 265: "UP",
    266: "PAGE_UP", 267: "PAGE_DOWN", 268: "HOME", 269: "END",
    280: "CAPS_LOCK", 281: "SCROLL_LOCK", 282: "NUM_LOCK",
    283: "PRINT_SCREEN", 284: "PAUSE",
    290: "F1", 291: "F2", 292: "F3", 293: "F4", 294: "F5", 295: "F6",
    296: "F7", 297: "F8", 298: "F9", 299: "F10", 300: "F11", 301: "F12",
    320: "NUMPAD_0", 321: "NUMPAD_1", 322: "NUMPAD_2", 323: "NUMPAD_3",
    324: "NUMPAD_4", 325: "NUMPAD_5", 326: "NUMPAD_6", 327: "NUMPAD_7",
    328: "NUMPAD_8", 329: "NUMPAD_9",
    330: "NUMPAD_DOT", 331: "NUMPAD_DIVIDE", 332: "NUMPAD_MULTIPLY",
    333: "NUMPAD_MINUS", 334: "NUMPAD_PLUS", 335: "NUMPAD_ENTER",
    336: "NUMPAD_EQUAL",
    340: "L_SHIFT", 341: "L_CTRL", 342: "L_ALT", 343: "L_SUPER",
    344: "R_SHIFT", 345: "R_CTRL", 346: "R_ALT", 347: "R_SUPER",
    348: "MENU", 256: "ESCAPE",
}
MOUSE_NAMES = {0: "LMB", 1: "RMB", 2: "MMB"}

def get_key_name(key_code: int) -> str:
    return GLFW_KEY_NAMES.get(key_code, f"K{key_code}")

def get_mouse_name(button: int) -> str:
    return MOUSE_NAMES.get(button, f"M{button}")

# === HUD elements ===
y = 5
line_h = 15
def next_line():
    global y
    y += line_h
    return y

t_ver  = Hud.add_text("", 5, next_line())
t_pos  = Hud.add_text("", 5, next_line())
t_fps  = Hud.add_text("", 5, next_line())
t_bio  = Hud.add_text("", 5, next_line())
t_dir  = Hud.add_text("", 5, next_line())
t_time = Hud.add_text("", 5, next_line())
t_ping = Hud.add_text("", 5, next_line())
t_mob  = Hud.add_text("", 5, next_line())
t_blk  = Hud.add_text("", 5, next_line())
t_inp  = Hud.add_text("", 5, next_line())
t_hand_main = Hud.add_text("", 5, next_line())
t_hand_off  = Hud.add_text("", 5, next_line())

Hud.use_toggle_key(True)
print("MicroHUD+ started. (toggle: F12)")

# === Direction helper ===
def yaw_to_direction(yaw: float) -> str:
    # Normalize yaw to -180 ~ 180
    yaw = ((yaw + 180) % 360) - 180
    
    # Minecraft基準（0=南, +90=西, ±180=北, -90=東）
    if -22.5 <= yaw < 22.5:
        return "South"
    elif 22.5 <= yaw < 67.5:
        return "South-West"
    elif 67.5 <= yaw < 112.5:
        return "West"
    elif 112.5 <= yaw < 157.5:
        return "North-West"
    elif yaw >= 157.5 or yaw < -157.5:
        return "North"
    elif -157.5 <= yaw < -112.5:
        return "North-East"
    elif -112.5 <= yaw < -67.5:
        return "East"
    elif -67.5 <= yaw < -22.5:
        return "South-East"

# === Biome getter ===
def get_biome_name():
    if mc.level is None or mc.player is None:
        return "Unknown"
    try:
        player_pos = mc.player.blockPosition()
        biome_holder = mc.level.getBiome(player_pos)
        biome_key = biome_holder.unwrapKey().get()
        return biome_key.location().toString().replace("minecraft:", "")
    except Exception:
        return "Unknown"

# === Input tracking ===
keys_pressed = set()
mouse_pressed = set()

eq = EventQueue()
eq.register_key_listener()
eq.register_mouse_listener()

def process_input_events():
    while True:
        e = eq.get()
        if e.type == EventType.KEY:
            if e.action == 1:
                keys_pressed.add(e.key)
            elif e.action == 0:
                keys_pressed.discard(e.key)
        elif e.type == EventType.MOUSE:
            if e.action == 1:
                mouse_pressed.add(e.button)
            elif e.action == 0:
                mouse_pressed.discard(e.button)
        sleep(0.01)

threading.Thread(target=process_input_events, daemon=True).start()

# === Main loop ===
while True:
    try:
        # === Version Info ===
        v = version_info()
        ver_text = f"VersionInfo : MC {v.minecraft} / MS {v.minescript} / {v.mod_loader} / {v.pyjinn}"

        # === Player Info ===
        x, y, z = [f"{p:.2f}" for p in player_position()]
        fps = mc.getFps()
        biome = get_biome_name()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ping = Server.get_ping()
        yaw, pitch = player_orientation()
        yaw = ((yaw + 180) % 360) - 180
        pitch = ((pitch + 180) % 360) - 180
        direction = yaw_to_direction(yaw)

        # === Entity & Block ===
        e = player_get_targeted_entity(20)
        mob_text = f"Mob: {e.type}" if e else "Mob: none"
        b = player_get_targeted_block(20)
        blk_text = f"Block: {b.type.replace('minecraft:', '')}" if b else "Block: none"

        # === Input ===
        key_names = [get_key_name(k) for k in keys_pressed]
        mouse_names = [get_mouse_name(b) for b in mouse_pressed]
        input_text = f"Keys: {', '.join(key_names) if key_names else 'None'} | Mouse: {', '.join(mouse_names) if mouse_names else 'None'}"

        # === Hands ===
        hands = m.player_hand_items()

        # main hand
        if hands.main_hand:
            main_item = hands.main_hand.get('item', 'minecraft:air') if isinstance(hands.main_hand, dict) else str(hands.main_hand)
            main_text = f"MainHand: {main_item.replace('minecraft:', '')}"
        else:
            main_text = "MainHand: empty"

        # off hand
        if hands.off_hand:
            off_item = hands.off_hand.get('item', 'minecraft:air') if isinstance(hands.off_hand, dict) else str(hands.off_hand)
            off_text = f"OffHand: {off_item.replace('minecraft:', '')}"
        else:
            off_text = "OffHand: empty"

        # === Update HUD ===
        Hud.set_text_string(t_ver,  ver_text)
        Hud.set_text_string(t_pos,  f"Pos: {x}, {y}, {z}")
        Hud.set_text_string(t_fps,  f"FPS: {fps}")
        Hud.set_text_string(t_bio,  f"Biome: {biome}")
        Hud.set_text_string(t_dir,  f"Dir: {direction} ({int(yaw)}°, {int(pitch)}°)")
        Hud.set_text_string(t_time, f"Time: {now}")
        Hud.set_text_string(t_ping, f"Ping: {ping if ping is not None else 'N/A'} ms")
        Hud.set_text_string(t_mob,  mob_text)
        Hud.set_text_string(t_blk,  blk_text)
        Hud.set_text_string(t_inp,  input_text)
        Hud.set_text_string(t_hand_main, main_text)
        Hud.set_text_string(t_hand_off,  off_text)

        sleep(0.1)

    except Exception as e:
        print(f"HUD Error: {e}")
        sleep(1)
```

## Memo

### **run.py**

```
A simple launcher script that executes multiple Minescript modules.
Used to load the HUD, chat logger, autofishing, advancement tracker,
damage debugger, and inventory tools at once.
```

### **chatlog_v0.0.01**

```
A basic chat logger that listens for chat events and writes all incoming
messages to a local text file with timestamps. Useful for debugging or
record-keeping on multiplayer servers.
```

### **microhud_v0.0.00 — v0.0.07**

```
A custom HUD overlay that gradually expands with new features. Across
each version, the HUD adds position, FPS, biome, direction, time,
server ping, targeted entity/block, input tracking, and hand items.
Later versions also refine direction calculation and improve layout.
```

### **autofish / fish_v0.0.01 – v0.0.02**

```
An automated fishing script that detects the bobber, waits for movement
indicating a bite, and reels in fish. Later versions include a random
AFK-prevention loop and smoother toggling using a keybind.
```

### **adv0_v0.0.02**

```
An advancement tracker that reads chat messages, detects advancement
events, assigns points, and records them in JSON. It also detects
first-time server-wide achievements and gives bonus points.
```

### **damageevent_v0.1.00**

```
A debugging tool that listens for damage events and prints detailed
information including entities involved, source type, distance, and
remaining health. It distinguishes environmental damage from combat.
```

### **steal_dump_v0.0.00**

```
An inventory helper that injects Steal and Dump buttons into container
screens. These buttons trigger quick-move operations to transfer items
in or out of inventories efficiently.
```

## Notes & Next Steps (Fishing + HUD)

**1) Direction Logic**

* Discovered a mismatch in yaw-to-direction mapping mid-development and corrected it.
* Verified against Minecraft’s coordinate system (0° = South, ±180° = North, +90° = West, −90° = East).
* Added tests/spot checks to avoid regressions.

**2) AFK Mitigation**

* Got kicked once due to inactivity.
* Implemented lightweight AFK prevention (periodic sneak/jump with random intervals).
* Keep it subtle to avoid server anti-cheat triggers.

**3) Multi-Angler Interference**

* Behavior becomes inconsistent when other players are fishing nearby (shared bobber detection and timing).
* Plan to harden detection (track local bobber by owner/UUID if available, fallback with distance/trajectory heuristics).
* Add timeouts and re-cast logic to recover from false positives.

**4) HUD Roadmap**

* Continue expanding HUD: hand items (done), targeted block/entity (done), ping/biome/time (done).
* Upcoming ideas: armor & durability, potion effects, light level, chunk coordinates, TPS estimate, actionbar/log overlay, minimal “raid/lag” mode.
* Focus on stability, layout readability, and low overhead.

**5) Action Items**

* [ ] Write a small validator for direction math (unit tests with boundary angles).
* [ ] Tag local bobber reliably; add distance + vertical-velocity thresholds.
* [ ] Add configurable AFK window and actions.
* [ ] Modularize HUD widgets and add toggles per widget.
* [ ] Log fishing state transitions for easier debugging.
