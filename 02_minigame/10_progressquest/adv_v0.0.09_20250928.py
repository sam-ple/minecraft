import minescript as m
from minescript import EventQueue, EventType
import re

player_advancements = {}
adv_pattern = re.compile(r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]")

eq = EventQueue()
eq.register_chat_listener()
m.echo("Chat listener ready!")

def save_adv_text():
    """全員の進捗リストをまとめてファイルに保存"""
    lines = []
    for player, advs in player_advancements.items():
        lines.append(f"{player}: {', '.join(advs)}")
    if not lines:
        lines = ["No advancements yet"]
    with open("adv_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

while True:
    event = eq.get()
    if not event or event.type != EventType.CHAT:
        continue

    msg = event.message

    # 進捗達成メッセージを検出
    match = adv_pattern.match(msg)
    if match:
        player_name, action, advancement_name = match.groups()
        if player_name not in player_advancements:
            player_advancements[player_name] = []
        if advancement_name not in player_advancements[player_name]:
            player_advancements[player_name].append(advancement_name)

        # デバッグ用チャット出力
        m.echo(f"{player_name} got '{advancement_name}'")

        # ファイルに保存（HUD用）
        save_adv_text()
