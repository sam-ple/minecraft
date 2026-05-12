import minescript as m
from minescript import EventQueue, EventType
import time  # ループ待機用

# イベントキュー初期化
eq = EventQueue()

# ダメージイベントを拾えるようにリスナー登録（必要な場合）
try:
    eq.register_damage_listener()
except:
    pass  # 環境によっては不要

# メインループ
while True:
    event = eq.get()
    if not event:
        time.sleep(0.01)
        continue

    # アイテム取得イベント
    if event.type == EventType.TAKE_ITEM:
        player_uuid = getattr(event, "player_uuid", "unknown_uuid")
        item_name = getattr(getattr(event, "item", None), "name", "unknown_item")
        amount = getattr(event, "amount", 1)

        # チャットに表示（{}をエスケープ）
        json_text = f'{{"text":"{player_uuid} picked up {amount}x {item_name}!"}}'
        m.execute(f'tellraw @a {json_text}')

    # ダメージイベント
    elif event.type == EventType.DAMAGE:
        attacker_uuid = getattr(event, "cause_uuid", "unknown_attacker")
        victim_uuid = getattr(event, "entity_uuid", "unknown_victim")
        source = getattr(event, "source", "unknown_source")

        json_text = f'{{"text":"{attacker_uuid} attacked {victim_uuid} using {source}!"}}'
        m.execute(f'tellraw @a {json_text}')
