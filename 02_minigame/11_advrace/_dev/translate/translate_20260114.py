import minescript as m
from minescript import EventQueue, EventType
import json
import re

# ------------------------------
# JSON 読み込み（英語→日本語）
# ------------------------------
with open("advancement.json", "r", encoding="utf-8") as f:
    ADV_JP = json.load(f)

# ------------------------------
# 英語チャットパターン
# ------------------------------
adv_pattern = re.compile(
    r"^(\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]"
)

# ------------------------------
# チャットに日本語で表示
# ------------------------------
def show_jp_advancement(player, adv_name):
    jp_name = ADV_JP.get(adv_name, adv_name)
    msg = f"🎉 {player} が実績達成: {jp_name}"
    m.execute(f'tellraw @a {json.dumps({"text": msg, "color": "gold"})}')

# ------------------------------
# チャットイベントループ
# ------------------------------
eq = EventQueue()
eq.register_chat_listener()

while True:
    event = eq.get()
    if event.type == EventType.CHAT:
        m_ = adv_pattern.match(event.message.strip())
        if m_:
            player, _, adv_name = m_.groups()
            show_jp_advancement(player, adv_name)
