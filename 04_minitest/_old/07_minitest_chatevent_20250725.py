import minescript as m
import queue
from minescript import EventQueue, EventType

def main():
    with EventQueue() as eq:
        eq.register_chat_listener()
        m.chat("✅ チャットイベントを待っています（--test を送ってみて）")
        while True:
            try:
                event = eq.get(timeout=3)
                if event.type == EventType.CHAT:
                    msg = event.message
                    # プレイヤー名除去
                    if ">" in msg:
                        msg = msg.split(">", 1)[1].strip()
                    msg = msg.lower()
                    m.log(f"📥 受信メッセージ: {msg}")
                    if msg == "--test":
                        m.chat("🎉 テスト成功！")
            except queue.Empty:
                m.log("⏳ チャットイベント待ち中...")

if __name__ == "__main__":
    main()

# -----------
# v0.0.1
# -----------
# import minescript as m
# from minescript import EventQueue, EventType

# m.echo("✅ チャットで '--start' を送るとメッセージを表示します。")

# with EventQueue() as eq:
#     eq.register_chat_listener()
#     while True:
#         event = eq.get()
#         if event.type == EventType.CHAT:
#             if "--start" in event.message.lower():
#                 m.execute('tellraw @a {"text":"ゲームを開始します！","color":"green","bold":true}')
