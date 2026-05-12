"""
Simple MicroHUD (Custom Layout)
"""

from time import sleep
from datetime import datetime
import sys

import minescript as m
from minescript import (
    player_position,
    player_orientation,
    player_get_targeted_block,
    version_info,
)
from java import JavaClass
from minescript_plus import Hud


# ============================================================
# Minecraft Client
# ============================================================
Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance()


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


t_version1 = Hud.add_text("", 5, next_y())
t_version2 = Hud.add_text("", 5, next_y())
t_time     = Hud.add_text("", 5, next_y())
t_pos      = Hud.add_text("", 5, next_y())
t_dir      = Hud.add_text("", 5, next_y())
t_biome    = Hud.add_text("", 5, next_y())
t_block    = Hud.add_text("", 5, next_y())

Hud.use_toggle_key(True)
print("Simple MicroHUD started (toggle: F12)")


# ============================================================
# Main Loop
# ============================================================
while True:
    try:
        # --- Version ---
        v = version_info()
        python_version = sys.version.split()[0]

        version_line1 = f"MC {v.minecraft} | MS {v.minescript} | Python {python_version}"
        version_line2 = f"{v.mod_loader} | {v.pyjinn}"

        # --- Time ---
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # --- Position ---
        px, py, pz = [f"{p:.2f}" for p in player_position()]

        # --- Direction ---
        yaw, pitch = player_orientation()
        yaw = ((yaw + 180) % 360) - 180
        pitch = ((pitch + 180) % 360) - 180
        direction = yaw_to_direction(yaw)

        # --- Biome ---
        biome = get_biome_name()

        # --- Target Block ---
        block = player_get_targeted_block(20)
        if block:
            bx, by, bz = block.position
            block_name = block.type.replace("minecraft:", "")
            block_text = f"{block_name} @ ({bx},{by},{bz})"
        else:
            block_text = "None"

        # --- HUD更新 ---
        Hud.set_text_string(t_version1, version_line1)
        Hud.set_text_string(t_version2, version_line2)
        Hud.set_text_string(t_time,  f"Time: {now}")
        Hud.set_text_string(t_pos,   f"Pos: {px}, {py}, {pz}")
        Hud.set_text_string(t_dir,   f"Dir: {direction} ({int(yaw)}°, {int(pitch)}°)")
        Hud.set_text_string(t_biome, f"Biome: {biome}")
        Hud.set_text_string(t_block, f"Block: {block_text}")

        sleep(0.1)

    except Exception as e:
        print(f"[SimpleHUD Error] {e}")
        sleep(1)
