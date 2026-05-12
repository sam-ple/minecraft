import minescript as m
from minescript import EventQueue, EventType
import time

# スパイグラス判定
def has_spyglass():
    hands = m.player_hand_items()
    if not hands or not hands.main_hand:
        return False
    item = hands.main_hand.get("item") if isinstance(hands.main_hand, dict) else str(hands.main_hand)
    return item == "minecraft:spyglass"

# 発射処理
def fire():
    target = m.player_get_targeted_entity(30)
    if target:
        # 即死ダメージ
        m.execute(f"damage {target.uuid} 100 minecraft:generic")
        # ちょっとだけ演出
        tx, ty, tz = target.position
        m.execute(f"particle minecraft:crit {tx} {ty+1} {tz} 0 0 0 0 30 force")
        m.execute(f"playsound minecraft:entity.player.attack.crit master @a {tx} {ty} {tz} 1 1")

# メイン
def main():
    m.echo("💀 STRESS MODE: Spyglass + Left Click = Instant Kill")

    with EventQueue() as eq:
        eq.register_mouse_listener()
        cooldown = 0

        while True:
            e = eq.get()
            if e.type == EventType.MOUSE and e.button == 0 and e.action == 1:
                if not has_spyglass():
                    continue
                now = time.time()
                if now - cooldown < 0.2:
                    continue
                cooldown = now
                fire()

main()
