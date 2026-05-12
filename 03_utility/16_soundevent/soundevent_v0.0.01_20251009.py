import json
import time
import minescript as m
from minescript_plus import Util

# JSON 読み込み
with open("soundevents_mapping.json", encoding="utf-8") as f:
    sounds = json.load(f)

# SoundEvents クラスを取得
se = Util.get_soundevents()

# 1つずつ再生
for entry in sounds:
    sound_name = entry["mojang"]
    try:
        # 文字列から属性を取得
        sound = getattr(se, sound_name)
        Util.play_sound(sound)
        m.chat(f"🔊 Playing: {sound_name}")
        time.sleep(0.8)  # 再生間隔（調整可能）
    except AttributeError:
        m.chat(f"⚠️ Not found: {sound_name}")
        continue

