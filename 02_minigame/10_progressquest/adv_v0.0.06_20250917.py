import minescript as ms

# プレイヤーごとのポイント
player_points = {}

# スコアボードを作成（存在しない場合のみ）
ms.execute("scoreboard objectives add AdvPoints dummy Points")
ms.execute("scoreboard objectives setdisplay sidebar AdvPoints")

with ms.EventQueue() as q:
    q.register_chat_listener()  # チャット監視

    while True:
        event = q.get()

        if event.type == ms.EventType.CHAT:
            msg = event.message

            # Advancement または Challenge の取得
            if "has made the advancement" in msg or "has completed the challenge" in msg:
                player_name = msg.split(" ")[0]

                # ポイント加算
                player_points[player_name] = player_points.get(player_name, 0) + 1

                # スコアボードに反映
                ms.execute(f"scoreboard players set {player_name} AdvPoints {player_points[player_name]}")

                # チャット通知
                ms.echo(f"{player_name} earned 1 point! (Total: {player_points[player_name]})")
