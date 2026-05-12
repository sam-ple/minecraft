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