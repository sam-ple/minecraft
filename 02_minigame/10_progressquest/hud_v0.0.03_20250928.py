from time import sleep
from minescript import player_position, echo
from java import JavaClass
from minescript_plus import Hud

Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance()

# HUD プレースホルダー
t_pos = Hud.add_text("Pos: ", 5, 5)
t_fps = Hud.add_text("FPS: ", 5, 15)

# 複数行分のプレースホルダーを用意
MAX_LINES = 10
t_adv_lines = [Hud.add_text("Adv: ", 5, 25 + i*10) for i in range(MAX_LINES)]
t_bio_lines = [Hud.add_text("Bio: ", 5, 25 + (MAX_LINES+i)*10) for i in range(MAX_LINES)]

Hud.use_toggle_key(True)
echo("Advancement & Biome HUD started. Use F12 to toggle.")

# ----------------------------
# txtファイル読み込み
# ----------------------------
def load_txt(filename, default="No data"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return default

# ----------------------------
# 文字列を折り返してリスト化
# ----------------------------
def wrap_text(text, max_chars):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

while True:
    x, y, z = [f"{p:.2f}" for p in player_position()]
    fps = mc.getFps()

    # HUDに表示するテキストを読み込み
    adv_text = load_txt("adv_output.txt", "No advancements yet")
    bio_text = load_txt("bio_output.txt", "No visited biomes")

    # 画面幅に応じて1行あたりの最大文字数を決定
    gui_width = mc.getWindow().getGuiScaledWidth()
    max_chars = max(10, gui_width // 6)

    # 文字列を折り返し
    adv_lines = wrap_text(adv_text, max_chars)
    bio_lines = wrap_text(bio_text, max_chars)

    # HUD 更新
    Hud.set_text(t_pos, f"Pos: {x}, {y}, {z}")
    Hud.set_text(t_fps, f"FPS: {fps}")

    # Advancements
    for i, hud_line in enumerate(t_adv_lines):
        if i < len(adv_lines):
            Hud.set_text(hud_line, adv_lines[i])
        else:
            Hud.set_text(hud_line, "")

    # Biomes
    for i, hud_line in enumerate(t_bio_lines):
        if i < len(bio_lines):
            Hud.set_text(hud_line, bio_lines[i])
        else:
            Hud.set_text(hud_line, "")

    sleep(0.1)
