import minescript as m
from minescript import EventQueue, EventType
import re

# プレイヤーごとのポイントと進捗
player_points = {}
player_advancements = {}

# スコアボード作成（存在しない場合のみ）
m.execute("scoreboard objectives add AdvPoints dummy Points")
m.execute("scoreboard objectives setdisplay sidebar AdvPoints")

# 進捗達成メッセージ用正規表現
adv_pattern = re.compile(r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]")

# イベントキュー
eq = EventQueue()
eq.register_chat_listener()
m.echo("Chat listener ready!")

def save_adv_text():
    """全員の進捗リスト＋スコアをまとめてファイルに保存"""
    lines = []
    for player, advs in player_advancements.items():
        score = player_points.get(player, 0)
        lines.append(f"{player} ({score}pts): {', '.join(advs)}")
    if not lines:
        lines = ["No advancements yet"]
    with open("adv_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

while True:
    event = eq.get()
    if not event or event.type != EventType.CHAT:
        continue

    msg = event.message.strip()

    # --- ?adv コマンド処理 ---
    if msg.startswith("<") and ">" in msg:
        player_name, content = msg[1:].split(">", 1)
        content = content.strip()

        if content.startswith("?adv"):
            parts = content.split()
            if len(parts) == 1:
                # 自分の進捗
                if player_name in player_advancements:
                    score = player_points.get(player_name, 0)
                    text = f"{player_name} ({score}pts): {', '.join(player_advancements[player_name])}"
                else:
                    text = f"{player_name} has no advancements yet."
                m.echo(text)
            elif len(parts) == 2:
                target = parts[1]
                if target in player_advancements:
                    score = player_points.get(target, 0)
                    text = f"{target} ({score}pts): {', '.join(player_advancements[target])}"
                else:
                    text = f"{target} has no advancements yet."
                m.echo(text)

    # --- 進捗達成メッセージを検出 ---
    match = adv_pattern.match(msg)
    if match:
        player_name, action, advancement_name = match.groups()

        # ポイント加算
        player_points[player_name] = player_points.get(player_name, 0) + 1

        # 進捗記録（重複防止）
        if player_name not in player_advancements:
            player_advancements[player_name] = []
        if advancement_name not in player_advancements[player_name]:
            player_advancements[player_name].append(advancement_name)

        # スコアボードに反映
        m.execute(f"scoreboard players set {player_name} AdvPoints {player_points[player_name]}")

        # デバッグ用チャット出力
        m.echo(f"{player_name} earned 1 point for '{advancement_name}'! (Total: {player_points[player_name]})")

        # HUD用ファイルに保存
        save_adv_text()
