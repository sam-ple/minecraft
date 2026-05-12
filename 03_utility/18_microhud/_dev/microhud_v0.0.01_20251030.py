# microhud_biome_time.py
import math
from time import sleep
from datetime import datetime
from minescript import player_position, echo
from java import JavaClass
from minescript_plus import Hud

# === Minecraft hooks ===
Minecraft = JavaClass("net.minecraft.client.Minecraft")
BlockPos = JavaClass("net.minecraft.core.BlockPos")
mc = Minecraft.getInstance()

# === HUD elements ===
t_pos = Hud.add_text("Pos: ", 5, 5)
t_fps = Hud.add_text("FPS: ", 5, 20)
t_bio = Hud.add_text("Biome: ", 5, 35)
t_time = Hud.add_text("Time: ", 5, 50)

Hud.use_toggle_key(True)
print("MicroHUD+ started. (toggle: F12)")

# === Biome getter ===
def get_biome_name():
    player_pos = mc.player.blockPosition()
    biome_holder = mc.level.getBiome(player_pos)
    biome_key = biome_holder.unwrapKey().get()
    return biome_key.location().toString()

# === Main loop ===
while True:
    # Player coordinates
    x, y, z = [f"{p:.2f}" for p in player_position()]
    fps = mc.getFps()
    biome = get_biome_name()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update HUD
    Hud.set_text_string(t_pos, f"Pos: {x}, {y}, {z}")
    Hud.set_text_string(t_fps, f"FPS: {fps}")
    Hud.set_text_string(t_bio, f"Biome: {biome}")
    Hud.set_text_string(t_time, f"Time: {now}")

    sleep(1)
