import minescript as m
import time
from minescript import EventQueue, EventType

# ==========================
# CONFIG（ここだけ編集）
# ==========================
CATCH_ITEM = "minecraft:stick"
CLICK_TYPE = "right"      # left / right
MAX_DISTANCE = 3
TP_HEIGHT = 320
# ==========================


def tell(msg, color="white"):
    m.execute(f'tellraw {m.player_name()} {{"text":"{msg}","color":"{color}"}}')


def get_main_hand_item():
    hands = m.player_hand_items()

    if not hands.main_hand:
        return "minecraft:air"

    if isinstance(hands.main_hand, dict):
        return hands.main_hand.get("item", "minecraft:air")

    return str(hands.main_hand)


def is_click_match(event):
    if event.type != EventType.MOUSE:
        return False

    # action == 1 → 押した瞬間
    if CLICK_TYPE == "left":
        return event.button == 0 and event.action == 1
    else:
        return event.button == 1 and event.action == 1


def get_spawn_egg(mob_type):
    if not mob_type.startswith("entity.minecraft."):
        return None
    base = mob_type.replace("entity.minecraft.", "")
    return f"minecraft:{base}_spawn_egg"


def catch_mob(entity):
    mob_type = entity.type
    egg = get_spawn_egg(mob_type)

    if not egg:
        tell("❌ Not a valid mob.", "red")
        return

    # 卵付与
    m.execute(f"give {m.player_name()} {egg} 1")
    tell(f"🥚 {egg} obtained!", "green")

    # 上空へ飛ばして消す
    try:
        m.execute(f"tp {entity.uuid} ~ {TP_HEIGHT} ~")
        time.sleep(0.05)
        m.execute(f"kill {entity.uuid}")
    except:
        m.execute(f"kill {entity.selector}")


def main():
    tell("🎯 Hold item and click mob to capture.", "aqua")

    with EventQueue() as eq:
        eq.register_mouse_listener()

        while True:
            event = eq.get()

            if not is_click_match(event):
                continue

            # 手持ちチェック
            main_item = get_main_hand_item()
            if main_item != CATCH_ITEM:
                continue

            target = m.player_get_targeted_entity(max_distance=MAX_DISTANCE)
            if target:
                catch_mob(target)
                time.sleep(0.3)


if __name__ == "__main__":
    main()
