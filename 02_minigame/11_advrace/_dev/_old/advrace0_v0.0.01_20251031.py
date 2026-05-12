import minescript as m
from minescript import EventQueue, EventType
import re
import json
import os

# ファイルパス（スクリプトと同じフォルダに保存）
SAVE_FILE = "advancement_points.json"

# 進捗メッセージ検出パターン
adv_pattern = re.compile(r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]")

eq = EventQueue()
eq.register_chat_listener()

# ファイル読み込み
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        points = json.load(f)
else:
    points = {}

# 初達成済み進捗の記録（リセットしてOK）
first_adv = set()

m.echo("📘 Advancement Tracker started! (self-only)")
m.echo(f"Loaded {len(points)} player records from {SAVE_FILE}")

def save_points():
    """ポイントをファイル保存"""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(points, f, indent=2, ensure_ascii=False)

while True:
    event = eq.get()
    if not event or event.type != EventType.CHAT:
        continue

    msg = event.message.strip()
    match = adv_pattern.match(msg)
    if not match:
        continue

    player, action, adv_name = match.groups()
    add_point = 1

    # 初達成ボーナス
    if adv_name not in first_adv:
        first_adv.add(adv_name)
        add_point += 1
        m.echo(f"✨ {player} got FIRST for '{adv_name}' (+1 bonus)")

    # ポイント加算
    points[player] = points.get(player, 0) + add_point
    save_points()

    # ログ的に追記出力（上書きしない）
    m.echo(f"📈 {player} now has {points[player]}pt ({'+' + str(add_point)})")
