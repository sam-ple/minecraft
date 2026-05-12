import json
import time
import minescript as m
from minescript_plus import Util, Gui

# --- 設定 ---
INTERVAL = 1.0  # 音と音の間隔（秒）

# --- JSON 読み込み ---
with open("soundevents_mapping.json", encoding="utf-8") as f:
    sounds = json.load(f)

# --- SoundEvents クラス取得 ---
se = Util.get_soundevents()

# --- タイトルタイミング設定（短め） ---
Gui.set_title_times(5, 40, 5)

for entry in sounds:
    mojang = entry["mojang"]
    yarn = entry["yarn"]

    try:
        sound = getattr(se, mojang)
    except AttributeError:
        continue

    # GUI表示
    display_text = f"§eMojang: §f{mojang} §7/ §bYarn: §f{yarn}"
    Gui.set_title("")  # タイトルは空
    Gui.set_subtitle(display_text)
    Gui.set_actionbar(display_text, tinted=True)

    # 再生
    Util.play_sound(sound)
    m.chat(f"🎵 {mojang}")

    time.sleep(INTERVAL)

# --- 完了メッセージ ---
Gui.clear_titles()
Gui.set_actionbar("✅ All sounds finished!", tinted=True)
m.chat("✅ All sounds finished!")
