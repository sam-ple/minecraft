import minescript as m
from minescript import EventQueue, EventType
import re
import json
import os

# 保存ファイル（同フォルダ内）
SAVE_FILE = "advancement_records.json"

# チャットの進捗メッセージを検出
adv_pattern = re.compile(r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]")

eq = EventQueue()
eq.register_chat_listener()

# データ読み込み
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)
else:
    records = {}

# 初達成チェック
first_adv = set(
    adv for player in records.values() for adv in player.get("advancements", [])
)

m.echo("📘 Advancement Tracker+ (self-only) started!")
m.echo(f"Loaded {len(records)} player records from {SAVE_FILE}")

def save_records():
    """ファイル保存"""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

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

    # データ初期化
    if player not in records:
        records[player] = {"points": 0, "advancements": []}

    # 初達成ボーナス
    if adv_name not in first_adv:
        first_adv.add(adv_name)
        add_point += 1
        m.echo(f"✨ {player} got FIRST for '{adv_name}' (+1 bonus)")

    # 重複取得はスキップ
    if adv_name not in records[player]["advancements"]:
        records[player]["advancements"].append(adv_name)
        records[player]["points"] += add_point
        save_records()

        m.echo(f"📈 {player}: +{add_point}pt (Total {records[player]['points']}) [{adv_name}]")
    else:
        m.echo(f"ℹ️ {player} already had '{adv_name}', skipped.")
