import json
import time
import minescript as m
from minescript_plus import Util, Gui

# --- 設定 ---
INTERVAL = 1.0  # 音と音の間隔（秒）
BOSSBAR_ID = "sound_display"

# --- JSON 読み込み ---
with open("soundevents_mapping.json", encoding="utf-8") as f:
    sounds = json.load(f)

# --- SoundEvents クラス取得 ---
se = Util.get_soundevents()

# --- ボスバー初期設定 ---
m.execute(f'bossbar add {BOSSBAR_ID} "Sound Display"')
m.execute(f'bossbar set {BOSSBAR_ID} color blue')
m.execute(f'bossbar set {BOSSBAR_ID} style notched_6')
m.execute(f'bossbar set {BOSSBAR_ID} players @a')
m.execute(f'bossbar set {BOSSBAR_ID} max {len(sounds)}')
m.execute(f'bossbar set {BOSSBAR_ID} value 0')

# --- タイトルタイミング設定 ---
Gui.set_title_times(5, 40, 5)

# --- 再生ループ ---
for i, entry in enumerate(sounds, 1):
    mojang = entry["mojang"]
    yarn = entry["yarn"]

    try:
        sound = getattr(se, mojang)
    except AttributeError:
        continue

    # 表示テキスト（§カラー対応）
    display_text = f"§eMojang: §f{mojang} §7/ §bYarn: §f{yarn}"

    # GUI表示更新
    Gui.set_title("")  # Titleは空
    Gui.set_subtitle(display_text)
    Gui.set_actionbar(display_text, tinted=True)

    # ボスバー更新
    m.execute(f'bossbar set {BOSSBAR_ID} name "{display_text}"')
    m.execute(f'bossbar set {BOSSBAR_ID} value {i}')

    # 再生＆チャット
    Util.play_sound(sound)
    Util.chat(f"🎵 {mojang}")

    time.sleep(INTERVAL)

# --- 終了処理 ---
Gui.clear_titles()
Gui.set_actionbar("✅ All sounds finished!", tinted=True)
Util.chat("✅ All sounds finished!")

# --- ボスバー完了演出 ---
m.execute(f'bossbar set {BOSSBAR_ID} name "✅ All sounds finished!"')
m.execute(f'bossbar set {BOSSBAR_ID} color green')
m.execute(f'bossbar set {BOSSBAR_ID} value {len(sounds)}')
time.sleep(3)
m.execute(f'bossbar remove {BOSSBAR_ID}')
