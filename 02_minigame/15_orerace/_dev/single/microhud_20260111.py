"""
Simple Target HUD +
- 視線の先（ブロック / モブ）
- 座標
- 方角
- バイオーム
"""

from time import sleep

import minescript as m
from minescript import (
    player_position,
    player_orientation,
    player_get_targeted_block,
    player_get_targeted_entity,
)
from java import JavaClass
from minescript_plus import Hud


# ============================================================
# Minecraft Instance
# ============================================================
Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance()


# ============================================================
# HUD レイアウト
# ============================================================
X = 5
Y = 5
LINE = 14

t_target   = Hud.add_text("", X, Y)
t_pos      = Hud.add_text("", X, Y + LINE)
t_dir      = Hud.add_text("", X, Y + LINE * 2)
t_biome    = Hud.add_text("", X, Y + LINE * 3)

Hud.use_toggle_key(True)
print("Simple Target HUD started (toggle: F12)")


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
def get_biome() -> str:
    if mc.level is None or mc.player is None:
        return "Unknown"
    try:
        pos = mc.player.blockPosition()
        biome = mc.level.getBiome(pos).unwrapKey().get()
        return biome.location().toString().replace("minecraft:", "")
    except Exception:
        return "Unknown"


# ============================================================
# メインループ
# ============================================================
while True:
    try:
        # --- 視線ターゲット ---
        entity = player_get_targeted_entity(20)
        block = player_get_targeted_block(20)

        if entity:
            target_text = f"Target: Mob ({entity.type.replace('minecraft:', '')})"
        elif block:
            target_text = f"Target: Block ({block.type.replace('minecraft:', '')})"
        else:
            target_text = ""

        # --- 座標 ---
        x, y, z = player_position()
        pos_text = f"Pos: {x:.1f}, {y:.1f}, {z:.1f}"

        # --- 方向 ---
        yaw, _ = player_orientation()
        direction = yaw_to_direction(yaw)
        dir_text = f"Dir: {direction} ({int(yaw)}°)"

        # --- バイオーム ---
        biome_text = f"Biome: {get_biome()}"

        # --- HUD 更新 ---
        Hud.set_text_string(t_target, target_text)
        Hud.set_text_string(t_pos, pos_text)
        Hud.set_text_string(t_dir, dir_text)
        Hud.set_text_string(t_biome, biome_text)

        sleep(0.05)

    except Exception as err:
        print(f"[SimpleTargetHUD] Error: {err}")
        sleep(1)
