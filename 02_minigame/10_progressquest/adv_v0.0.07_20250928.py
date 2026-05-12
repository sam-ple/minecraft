import minescript as ms
import re

# プレイヤーごとのポイントと進捗
player_points = {}
player_advancements = {}

# スコアボードを作成（存在しない場合のみ）
ms.execute("scoreboard objectives add AdvPoints dummy Points")
ms.execute("scoreboard objectives setdisplay sidebar AdvPoints")

# 正規表現パターン
adv_pattern = re.compile(r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]")

with ms.EventQueue() as q:
    q.register_chat_listener()  # チャット監視

    while True:
        event = q.get()

        if event.type == ms.EventType.CHAT:
            msg = event.message

            # メッセージから進捗を抽出
            match = adv_pattern.match(msg)
            if match:
                player_name, action, advancement_name = match.groups()

                # ポイント加算
                player_points[player_name] = player_points.get(player_name, 0) + 1

                # 進捗を記録（重複防止）
                if player_name not in player_advancements:
                    player_advancements[player_name] = []
                if advancement_name not in player_advancements[player_name]:
                    player_advancements[player_name].append(advancement_name)

                # スコアボードに反映
                ms.execute(f"scoreboard players set {player_name} AdvPoints {player_points[player_name]}")

                # チャット通知
                ms.echo(f"{player_name} earned 1 point for '{advancement_name}'! (Total: {player_points[player_name]})")

                # デバッグ表示（保存済み進捗一覧）
                ms.echo(f"{player_name}'s advancements: {', '.join(player_advancements[player_name])}")
