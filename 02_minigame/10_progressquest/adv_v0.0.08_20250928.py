import minescript as m
from minescript import EventQueue, EventType
import re

# --- データ保持 ---
player_advancements = {}

# --- 正規表現で進捗達成を検出 ---
adv_pattern = re.compile(r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]")

eq = EventQueue()
eq.register_chat_listener()
m.echo("Chat listener ready!")

while True:
    event = eq.get()
    if not event or event.type != EventType.CHAT:
        continue

    msg = event.message

    # --- 進捗達成メッセージの処理 ---
    match = adv_pattern.match(msg)
    if match:
        player_name, action, advancement_name = match.groups()
        if player_name not in player_advancements:
            player_advancements[player_name] = []
        if advancement_name not in player_advancements[player_name]:
            player_advancements[player_name].append(advancement_name)
        m.echo(f"{player_name}'s advancements: {', '.join(player_advancements[player_name])}")
        continue

    # --- 通常チャットからのコマンド処理 ---
    # 例: <crocadooo> ?adv
    #     <crocadooo> ?adv playername
    if msg.startswith("<") and ">" in msg:
        player_name, content = msg[1:].split(">", 1)
        content = content.strip()

        if content.startswith("?adv"):
            parts = content.split()
            if len(parts) == 1:
                # 自分の進捗を表示
                if player_name in player_advancements:
                    m.echo(f"{player_name}'s advancements: {', '.join(player_advancements[player_name])}")
                else:
                    m.echo(f"{player_name} has no advancements yet.")
            elif len(parts) == 2:
                target = parts[1]
                if target in player_advancements:
                    m.echo(f"{target}'s advancements: {', '.join(player_advancements[target])}")
                else:
                    m.echo(f"{target} has no advancements yet.")
