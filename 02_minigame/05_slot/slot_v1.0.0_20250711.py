import minescript as m
import time
from threading import Thread
import json

# === スロット設定 ===
egg_list = [
    "minecraft:iron_golem_spawn_egg",
    "minecraft:blaze_spawn_egg",
    "minecraft:zombie_spawn_egg",
    "minecraft:creeper_spawn_egg",
    "minecraft:skeleton_spawn_egg",
    "minecraft:slime_spawn_egg"
]

block_list = [
    "minecraft:iron_ore",
    "minecraft:gold_ore",
    "minecraft:diamond_ore",
    "minecraft:copper_ore",
    "minecraft:coal_ore",
    "minecraft:lapis_ore"
]

plushie_list = [
    "plushie_buddies:plushie_breeze",
    "plushie_buddies:plushie_sniffer",
    "plushie_buddies:plushie_allay",
    "plushie_buddies:plushie_enderman",
    "plushie_buddies:plushie_zombie",
]

# 選択するスロット内容
slot_list = egg_list  # ← egg_list, block_list, plushie_list から選べる

rolling = [False, False, False]
stop_flag = False
results = ["", "", ""]

# === 向きと位置取得（プレイヤーの背面に表示） ===
def get_frame_positions_and_facing():
    x, y, z = m.player_position()
    yaw, _ = m.player_orientation()
    x, y, z = int(x), int(y), int(z)

    if 45 <= yaw < 135:      # 西向き → 東側に表示
        facing = 0  # East
        positions = [(x+1, y+1, z+1), (x+1, y+1, z), (x+1, y+1, z-1)]
    elif 135 <= yaw < 225:   # 北向き → 南側に表示
        facing = 2  # South
        positions = [(x+1, y+1, z+1), (x, y+1, z+1), (x-1, y+1, z+1)]
    elif 225 <= yaw < 315:   # 東向き → 西側に表示
        facing = 1  # West
        positions = [(x-1, y+1, z-1), (x-1, y+1, z), (x-1, y+1, z+1)]
    else:                    # 南向き → 北側に表示
        facing = 3  # North
        positions = [(x-1, y+1, z-1), (x, y+1, z-1), (x+1, y+1, z-1)]

    return positions, facing

# === アイテムフレームの初期設置 ===
def setup_item_frames(positions, facing):
    for i in range(3):
        m.execute(f'kill @e[type=item_frame,tag=slot_{i}]')

    for i, pos in enumerate(positions):
        x, y, z = pos
        m.execute(
            f'summon item_frame {x} {y} {z} '
            f'{{Facing:{facing},Item:{{id:"{slot_list[0]}",Count:1}},Invisible:1b,Fixed:1b,Tags:["slot_{i}"]}}'
        )

# === アイテムと結果を更新 ===
def update_item_frame(index, item_id):
    m.execute(
        f'data modify entity @e[type=item_frame,tag=slot_{index},limit=1,sort=nearest] '
        f'Item set value {{id:"{item_id}",Count:1b}}'
    )

def update_item_frame_and_result(index, item_id):
    update_item_frame(index, item_id)
    results[index] = item_id

# === スロット回転処理 ===
def roll_slot(index):
    idx = 0
    while rolling[index] and not stop_flag:
        item_id = slot_list[idx % len(slot_list)]
        update_item_frame_and_result(index, item_id)
        idx += 1
        time.sleep(0.2)

# === 名前整形 ===
def format_name(item_id: str) -> str:
    if slot_list == egg_list:
        return item_id.split(":")[1].replace("_spawn_egg", "").replace("_", " ").title()
    elif slot_list == block_list:
        return item_id.split(":")[1].replace("_", " ").title()
    elif slot_list == plushie_list:
        return item_id.split(":")[1].replace("plushie_", "").replace("_", " ").title() + " Plushie"
    else:
        return item_id

# === サブタイトル表示更新（???対応） ===
def update_subtitle(final=False):
    m.execute('title @a clear')

    names = []
    for i in range(3):
        if not rolling[i] and results[i]:
            names.append(format_name(results[i]))
        else:
            names.append("???")

    text = " + ".join(names)
    subtitle_json = json.dumps({"text": text, "color": "aqua"})

    m.execute('title @a title {"text":" ", "color":"white"}')
    m.execute(f'title @a subtitle {subtitle_json}')

    if final:
        time.sleep(0.4)
        if len(set(results)) == 1 and results[0] != "":
            jackpot_name = format_name(results[0])
            title_json = json.dumps({
#                "text": f"🎉 JACKPOT! {jackpot_name}! 🎉",
                "text": f"🎉 JACKPOT! 🎉",
                "color": "gold",
                "bold": True
            })
            m.execute(f"title @a title {title_json}")
            m.execute('playsound minecraft:entity.player.levelup master @a')
            m.execute('particle minecraft:firework ~ ~2 ~ 0.5 1 0.5 0.01 50')

# === 1回分の実行 ===
def run_once():
    global rolling, stop_flag, results
    stop_flag = False
    rolling = [True, True, True]
    results = ["", "", ""]

    positions, facing = get_frame_positions_and_facing()
    setup_item_frames(positions, facing)

    m.echo("Slots are rolling! Press Enter to stop each slot!")

    threads = []
    for i in range(3):
        t = Thread(target=roll_slot, args=(i,), daemon=True)
        t.start()
        threads.append(t)

    with m.EventQueue() as eq:
        eq.register_key_listener()
        idx = 0
        while idx < 3 and not stop_flag:
            event = eq.get()
            if event.type == m.EventType.KEY and event.action == 0 and event.key == 257:
                rolling[idx] = False
                time.sleep(0.3)
                update_subtitle(final=(idx == 2))
                idx += 1

# === メインループ ===
def main():
    global stop_flag
    m.echo("Block Slot Machine Started!")
    m.echo("Press Enter to stop each slot. Type 'stop' in chat to end.")

    while True:
        run_once()
        m.echo("Type 'stop' in chat to end the round, or press Enter to restart.")

        stop_flag = False
        with m.EventQueue() as eq:
            eq.register_key_listener()
            eq.register_chat_listener()
            while True:
                event = eq.get()
                if event.type == m.EventType.CHAT and "stop" in event.message.lower():
                    stop_flag = True
                    m.echo("'stop' received. Exiting...")
                    return
                if event.type == m.EventType.KEY and event.action == 0 and event.key == 257:
                    break

main()