"""
MicroHUD

Based on the original MicroHUD script by RazrCraft (GitHub: @R4z0rX), the creator of Minescript Plus.

Original source:
https://discord.com/channels/930220988472389713/1068545062646059128/threads/1414377991395610646
"""

from time import sleep
from datetime import datetime
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
# Minecraft Client Hook
# ============================================================
Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance()


# ============================================================
# GLFW Key / Mouse Name Tables
# ============================================================
GLFW_KEY_NAMES = {
    32: "SPACE", 39: "'", 44: ",", 45: "-", 46: ".", 47: "/",
    48: "0", 49: "1", 50: "2", 51: "3", 52: "4", 53: "5",
    54: "6", 55: "7", 56: "8", 57: "9",
    59: ";", 61: "=", 65: "A", 66: "B", 67: "C", 68: "D",
    69: "E", 70: "F", 71: "G", 72: "H", 73: "I",
    74: "J", 75: "K", 76: "L", 77: "M", 78: "N",
    79: "O", 80: "P", 81: "Q", 82: "R", 83: "S",
    84: "T", 85: "U", 86: "V", 87: "W", 88: "X",
    89: "Y", 90: "Z",
    91: "[", 92: "\\", 93: "]", 96: "`",
    257: "ENTER", 258: "TAB", 259: "BACKSPACE",
    262: "RIGHT", 263: "LEFT", 264: "DOWN", 265: "UP",
    266: "PAGE_UP", 267: "PAGE_DOWN",
    268: "HOME", 269: "END",
    280: "CAPS_LOCK", 281: "SCROLL_LOCK", 282: "NUM_LOCK",
    283: "PRINT_SCREEN", 284: "PAUSE",
    290: "F1", 291: "F2", 292: "F3", 293: "F4",
    294: "F5", 295: "F6", 296: "F7", 297: "F8",
    298: "F9", 299: "F10", 300: "F11", 301: "F12",
    340: "L_SHIFT", 341: "L_CTRL", 342: "L_ALT",
    344: "R_SHIFT", 345: "R_CTRL", 346: "R_ALT",
    256: "ESCAPE",
}

MOUSE_NAMES = {
    0: "LMB",
    1: "RMB",
    2: "MMB",
}


def get_key_name(key_code: int) -> str:
    """Convert GLFW key code to readable name."""
    return GLFW_KEY_NAMES.get(key_code, f"K{key_code}")


def get_mouse_name(button: int) -> str:
    """Convert mouse button code to readable name."""
    return MOUSE_NAMES.get(button, f"M{button}")


# ============================================================
# HUD Layout
# ============================================================
START_Y = 5
LINE_HEIGHT = 10
_current_y = START_Y


def next_line_y() -> int:
    """Return next Y position for HUD text."""
    global _current_y
    y = _current_y
    _current_y += LINE_HEIGHT
    return y


t_version   = Hud.add_text("", 5, next_line_y())
t_position  = Hud.add_text("", 5, next_line_y())
t_fps       = Hud.add_text("", 5, next_line_y())
t_biome     = Hud.add_text("", 5, next_line_y())
t_direction = Hud.add_text("", 5, next_line_y())
t_time      = Hud.add_text("", 5, next_line_y())
t_ping      = Hud.add_text("", 5, next_line_y())
t_entity    = Hud.add_text("", 5, next_line_y())
t_block     = Hud.add_text("", 5, next_line_y())
t_input     = Hud.add_text("", 5, next_line_y())
t_mainhand  = Hud.add_text("", 5, next_line_y())
t_offhand   = Hud.add_text("", 5, next_line_y())

Hud.use_toggle_key(True)
print("MicroHUD started (toggle: F12)")


# ============================================================
# Direction Helper
# ============================================================
def yaw_to_direction(yaw: float) -> str:
    """
    Convert Minecraft yaw to compass direction.
    Minecraft yaw: 0 = South, +90 = West, ±180 = North, -90 = East
    """
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
# Biome Helper
# ============================================================
# def get_biome_name() -> str:
#     """Return the biome name the player is currently in."""
#     if mc.level is None or mc.player is None:
#         return "Unknown"
#     try:
#         pos = mc.player.blockPosition()
#         biome = mc.level.getBiome(pos).unwrapKey().get()
#         return biome.location().toString().replace("minecraft:", "")
#     except Exception:
#         return "Unknown"

import json

# 外部 JSON を読み込む
with open("biome.json", "r", encoding="utf-8") as f:
    BIOME_JP = json.load(f)

def get_biome_name() -> str:
    """Return the biome name the player is currently in as 英語（日本語）."""
    if mc.level is None or mc.player is None:
        return "Unknown"
    try:
        pos = mc.player.blockPosition()
        biome = mc.level.getBiome(pos).unwrapKey().get()
        biome_id = biome.location().toString().replace("minecraft:", "")
        jp_name = BIOME_JP.get(biome_id, "不明")
        return f"{biome_id}（{jp_name}）"
    except Exception:
        return "Unknown"

# ============================================================
# Input Tracking (Keyboard & Mouse)
# ============================================================
keys_pressed = set()
mouse_pressed = set()

event_queue = EventQueue()
event_queue.register_key_listener()
event_queue.register_mouse_listener()


def input_event_loop():
    """Continuously process input events."""
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

        sleep(0.02)


threading.Thread(target=input_event_loop, daemon=True).start()


# ============================================================
# Main HUD Update Loop
# ============================================================
while True:
    try:
        # --- Version Info ---
        v = version_info()
        version_text = (
            f"Version: MC {v.minecraft} | MS {v.minescript} | "
            f"{v.mod_loader} | {v.pyjinn}"
        )

        # --- Player Info ---
        px, py, pz = [f"{p:.2f}" for p in player_position()]
        fps = mc.getFps()
        biome = get_biome_name()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ping = Server.get_ping()

        yaw, pitch = player_orientation()
        yaw = ((yaw + 180) % 360) - 180
        pitch = ((pitch + 180) % 360) - 180
        direction = yaw_to_direction(yaw)

        # --- Targeted Entity / Block ---
        entity = player_get_targeted_entity(20)
        block = player_get_targeted_block(20)

        entity_text = f"Mob: {entity.type}" if entity else "Mob: none"
        block_text = (
            f"Block: {block.type.replace('minecraft:', '')}"
            if block else "Block: none"
        )

        # --- Input State ---
        key_text = ", ".join(sorted(get_key_name(k) for k in keys_pressed)) or "None"
        mouse_text = ", ".join(sorted(get_mouse_name(b) for b in mouse_pressed)) or "None"
        input_text = f"Keys: {key_text} | Mouse: {mouse_text}"

        # --- Hand Items ---
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

        # --- Update HUD ---
        Hud.set_text_string(t_version, version_text)
        Hud.set_text_string(t_position, f"Pos: {px}, {py}, {pz}")
        Hud.set_text_string(t_fps, f"FPS: {fps}")
        Hud.set_text_string(t_biome, f"Biome: {biome}")
        Hud.set_text_string(
            t_direction, f"Dir: {direction} ({int(yaw)}°, {int(pitch)}°)"
        )
        Hud.set_text_string(t_time, f"Time: {now}")
        Hud.set_text_string(
            t_ping, f"Ping: {ping if ping is not None else 'N/A'} ms"
        )
        Hud.set_text_string(t_entity, entity_text)
        Hud.set_text_string(t_block, block_text)
        Hud.set_text_string(t_input, input_text)
        Hud.set_text_string(
            t_mainhand, f"MainHand: {str(main_item).replace('minecraft:', '')}"
        )
        Hud.set_text_string(
            t_offhand, f"OffHand: {str(off_item).replace('minecraft:', '')}"
        )

        sleep(0.1)

    except Exception as err:
        print(f"[MicroHUD+] Error: {err}")
        sleep(1)
