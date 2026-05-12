"""
MicroHUD

Based on the original MicroHUD script by RazrCraft (GitHub: @R4z0rX), the creator of Minescript Plus.

Original source:
https://discord.com/channels/930220988472389713/1068545062646059128/threads/1414377991395610646

Extended HUD for Minescript
- Version
- Time
- Position
- Direction
- Biome 確認 (1.21.11では正確に取得できない可能性あり
- Target Block
- Target Mob
- FPS
- Ping
- Hand Items
- Key / Mouse Input (with key codes)
"""

# ============================================================
# Imports
# ============================================================

from time import sleep
from datetime import datetime
import sys
import threading

import minescript as m
from minescript import (
    player_position,
    player_orientation,
    player_get_targeted_block,
    player_get_targeted_entity,
    version_info,
    EventQueue,
    EventType,
)

from java import JavaClass
from minescript_plus import Hud, Server


# ============================================================
# Minecraft Client
# ============================================================

Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance()


# ============================================================
# GLFW Key / Mouse Name Tables
# ============================================================

GLFW_KEY_NAMES = {
    32: "SPACE",
    65: "A", 66: "B", 67: "C", 68: "D",
    69: "E", 70: "F", 71: "G", 72: "H",
    73: "I", 74: "J", 75: "K", 76: "L",
    77: "M", 78: "N", 79: "O", 80: "P",
    81: "Q", 82: "R", 83: "S", 84: "T",
    85: "U", 86: "V", 87: "W", 88: "X",
    89: "Y", 90: "Z",

    257: "ENTER",
    258: "TAB",
    259: "BACKSPACE",

    262: "RIGHT",
    263: "LEFT",
    264: "DOWN",
    265: "UP",

    290: "F1", 291: "F2", 292: "F3",
    293: "F4", 294: "F5", 295: "F6",
    296: "F7", 297: "F8", 298: "F9",
    299: "F10", 300: "F11", 301: "F12",
}

MOUSE_NAMES = {
    0: "LMB",
    1: "RMB",
    2: "MMB",
}


def get_key_name_code(key_code: int) -> str:
    name = GLFW_KEY_NAMES.get(key_code, f"K{key_code}")
    return f"{name}({key_code})"


def get_mouse_name(button: int) -> str:
    return MOUSE_NAMES.get(button, f"M{button}")


# ============================================================
# Input Tracking
# ============================================================

keys_pressed = set()
mouse_pressed = set()

event_queue = EventQueue()
event_queue.register_key_listener()
event_queue.register_mouse_listener()


def input_event_loop():

    while True:

        event = event_queue.get()

        if event.type == EventType.KEY:

            if event.action == 1:
                keys_pressed.add(event.key)

            elif event.action == 0:
                keys_pressed.discard(event.key)

        elif event.type == EventType.MOUSE:

            if event.action == 1:
                mouse_pressed.add(event.button)

            elif event.action == 0:
                mouse_pressed.discard(event.button)

        sleep(0.03)


threading.Thread(target=input_event_loop, daemon=True).start()


# ============================================================
# 方角変換
# ============================================================

def yaw_to_direction(yaw: float) -> str:

    yaw = ((yaw + 180) % 360) - 180

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


# ============================================================
# バイオーム取得
# ============================================================

def get_biome_name():

    if mc.level is None or mc.player is None:
        return "Unknown"

    try:
        pos = mc.player.blockPosition()
        biome = mc.level.getBiome(pos).unwrapKey().get()
        return biome.location().toString().replace("minecraft:", "")

    except Exception:
        return "Unknown"


# ============================================================
# HUDレイアウト
# ============================================================

START_Y = 15
LINE_HEIGHT = 12
current_y = START_Y


def next_y():

    global current_y
    y = current_y
    current_y += LINE_HEIGHT
    return y


# ============================================================
# HUD要素
# ============================================================

t_version1 = Hud.add_text("", 5, next_y())
t_version2 = Hud.add_text("", 5, next_y())

t_time = Hud.add_text("", 5, next_y())
t_pos = Hud.add_text("", 5, next_y())
t_dir = Hud.add_text("", 5, next_y())
t_biome = Hud.add_text("", 5, next_y())

t_block = Hud.add_text("", 5, next_y())
t_mob = Hud.add_text("", 5, next_y())

t_fps = Hud.add_text("", 5, next_y())
t_ping = Hud.add_text("", 5, next_y())

t_input = Hud.add_text("", 5, next_y())

t_mainhand = Hud.add_text("", 5, next_y())
t_offhand = Hud.add_text("", 5, next_y())


Hud.use_toggle_key(True)
print("MicroHUD+ started (toggle: F12)")


# ============================================================
# Main Loop
# ============================================================

while True:

    try:

        # Version
        v = version_info()
        python_version = sys.version.split()[0]

        version_line1 = f"MC {v.minecraft} | MS {v.minescript} | Python {python_version}"
        version_line2 = f"{v.mod_loader} | {v.pyjinn}"

        # Time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Position
        px, py, pz = [f"{p:.2f}" for p in player_position()]

        # Direction
        yaw, pitch = player_orientation()

        yaw = ((yaw + 180) % 360) - 180
        pitch = ((pitch + 180) % 360) - 180

        direction = yaw_to_direction(yaw)

        # Biome
        biome = get_biome_name()

        # Target Block
        block = player_get_targeted_block(20)

        if block:
            bx, by, bz = block.position
            block_name = block.type.replace("minecraft:", "")
            block_text = f"{block_name} @ ({bx},{by},{bz})"
        else:
            block_text = "None"

        # Target Mob
        entity = player_get_targeted_entity(20)
        mob_text = entity.type if entity else "None"

        # FPS
        fps = mc.getFps()

        # Ping
        ping = Server.get_ping()

        # Input
        key_text = ", ".join(sorted(get_key_name_code(k) for k in keys_pressed)) or "None"
        mouse_text = ", ".join(sorted(get_mouse_name(b) for b in mouse_pressed)) or "None"
        input_text = f"Keys: {key_text} | Mouse: {mouse_text}"

        # Hand Items
        hands = m.player_hand_items()

        main_item = (
            hands.main_hand.get("item", "minecraft:air")
            if isinstance(hands.main_hand, dict)
            else hands.main_hand
        )

        off_item = (
            hands.off_hand.get("item", "minecraft:air")
            if isinstance(hands.off_hand, dict)
            else hands.off_hand
        )

        # ====================================================
        # HUD更新
        # ====================================================

        Hud.set_text_string(t_version1, version_line1)
        Hud.set_text_string(t_version2, version_line2)

        Hud.set_text_string(t_time, f"Time: {now}")

        Hud.set_text_string(t_pos, f"Pos: {px}, {py}, {pz}")

        Hud.set_text_string(
            t_dir,
            f"Dir: {direction} ({int(yaw)}°, {int(pitch)}°)"
        )

        Hud.set_text_string(t_biome, f"Biome: {biome}")

        Hud.set_text_string(t_block, f"Block: {block_text}")

        Hud.set_text_string(t_mob, f"Mob: {mob_text}")

        Hud.set_text_string(t_fps, f"FPS: {fps}")

        Hud.set_text_string(
            t_ping,
            f"Ping: {ping if ping else 'N/A'} ms"
        )

        Hud.set_text_string(t_input, input_text)

        Hud.set_text_string(
            t_mainhand,
            f"MainHand: {str(main_item).replace('minecraft:', '')}"
        )

        Hud.set_text_string(
            t_offhand,
            f"OffHand: {str(off_item).replace('minecraft:', '')}"
        )

        sleep(0.1)

    except Exception as e:

        print(f"[MicroHUD Error] {e}")
        sleep(1)
