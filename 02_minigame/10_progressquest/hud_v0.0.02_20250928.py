from time import sleep
from minescript import player_position, echo
from java import JavaClass
from minescript_plus import Hud

Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance()

# HUD プレースホルダー
t_pos = Hud.add_text("Pos: ", 5, 5)
t_fps = Hud.add_text("FPS: ", 5, 15)

# 複数行分のプレースホルダーを用意（5行まで表示）
t_adv_lines = [Hud.add_text("", 5, 25 + i*10) for i in range(5)]

Hud.use_toggle_key(True)
echo("Advancement HUD started. Use F12 to toggle.")

def load_adv_text():
    try:
        with open("adv_output.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "No advancements yet"

def wrap_text(text, max_chars):
    """指定文字数ごとに改行してリスト化"""
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

while True:
    x, y, z = [f"{p:.2f}" for p in player_position()]
    fps = mc.getFps()
    adv_text = load_adv_text()

    # 画面幅に応じて1行の最大文字数を決定
    gui_width = mc.getWindow().getGuiScaledWidth()
    max_chars = max(10, gui_width // 6)

    # 折り返し
    lines = wrap_text(adv_text, max_chars)

    # HUD 更新
    Hud.set_text(t_pos, f"Pos: {x}, {y}, {z}")
    Hud.set_text(t_fps, f"FPS: {fps}")

    for i, hud_line in enumerate(t_adv_lines):
        if i < len(lines):
            Hud.set_text(hud_line, lines[i])
        else:
            Hud.set_text(hud_line, "")  # 余分な行は消す

    sleep(0.1)
