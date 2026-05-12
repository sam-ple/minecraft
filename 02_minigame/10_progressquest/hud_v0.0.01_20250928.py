from time import sleep
from minescript import player_position, echo
from java import JavaClass
from minescript_plus import Hud

Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance()

# HUD プレースホルダー
t_pos = Hud.add_text("Pos: ", 5, 5)
t_fps = Hud.add_text("FPS: ", 5, 15)
t_adv = Hud.add_text("Adv: ", 5, 25)

Hud.use_toggle_key(True)
echo("Advancement HUD started. Use F12 to toggle.")

def load_adv_text():
    try:
        with open("adv_output.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "No advancements yet"

while True:
    x, y, z = [f"{p:.2f}" for p in player_position()]
    fps = mc.getFps()
    adv_text = load_adv_text()

    Hud.set_text(t_pos, f"Pos: {x}, {y}, {z}")
    Hud.set_text(t_fps, f"FPS: {fps}")
    Hud.set_text(t_adv, adv_text)

    sleep(0.1)
