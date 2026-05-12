import minescript as ms

# ポイントを保持する辞書
player_points = {}

with ms.EventQueue() as q:
    q.register_chat_listener()  # チャット監視

    while True:
        event = q.get()

        # 進捗達成メッセージを検出 (英語クライアント)
        if event.type == ms.EventType.CHAT and "has made the advancement [Diamonds!]" in event.message:
            # "PlayerName has made the advancement [Diamonds!]" の形式
            player_name = event.message.split(" ")[0]

            # ポイント加算
            player_points[player_name] = player_points.get(player_name, 0) + 10

            # 通知
            ms.echo(f"{player_name} earned 10 points! (Total: {player_points[player_name]})")
