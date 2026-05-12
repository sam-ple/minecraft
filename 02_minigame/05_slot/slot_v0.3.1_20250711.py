import minescript as m
import time
from threading import Thread

# === Settings ===
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
    "plushie_buddies:plushie_allay"
]

# ここを切り替えてスロットの中身を変更
slot_list = egg_list  # egg_list, block_list, plushie_list から選ぶ

rolling = [False, False, False]
stop_flag = False
results = ["", "", ""]

# === Get positions and facing for 3 item frames ===
def get_frame_positions_and_facing():
    x, y, z = m.player_position()
    yaw, _ = m.player_orientation()
    x, y, z = int(x), int(y), int(z)

    if 45 <= yaw < 135:      # West
        facing = 1
        positions = [(x-1, y+1, z-1), (x-1, y+1, z), (x-1, y+1, z+1)]
    elif 135 <= yaw < 225:   # North
        facing = 3
        positions = [(x-1, y+1, z-1), (x, y+1, z-1), (x+1, y+1, z-1)]
    elif 225 <= yaw < 315:   # East
        facing = 0
        positions = [(x+1, y+1, z+1), (x+1, y+1, z), (x+1, y+1, z-1)]
    else:                    # South
        facing = 2
        positions = [(x+1, y+1, z+1), (x, y+1, z+1), (x-1, y+1, z+1)]

    return positions, facing

# === Setup item frames once ===
def setup_item_frames(positions, facing):
    # Cleanup previous frames
    m.execute('kill @e[type=item_frame,tag=slot_0]')
    m.execute('kill @e[type=item_frame,tag=slot_1]')
    m.execute('kill @e[type=item_frame,tag=slot_2]')

    for i, pos in enumerate(positions):
        x, y, z = pos
        # 初期アイテムはslot_listの最初のアイテムで統一
        m.execute(
            f'summon item_frame {x} {y} {z} '
            f'{{Facing:{facing},Item:{{id:"{slot_list[0]}",Count:1}},Invisible:1b,Fixed:1b,Tags:["slot_{i}"]}}'
        )

# === Update content only (lightweight) ===
def update_item_frame(index, item_id):
    m.execute(
        f'data modify entity @e[type=item_frame,tag=slot_{index},limit=1,sort=nearest] '
        f'Item set value {{id:"{item_id}",Count:1b}}'
    )

# === Roll one slot ===
def roll_slot(index):
    idx = 0
    while rolling[index] and not stop_flag:
        item_id = slot_list[idx % len(slot_list)]
        update_item_frame(index, item_id)
        results[index] = item_id
        idx += 1
        time.sleep(0.2)

# === 名前整形関数 ===
def format_name(item_id: str) -> str:
    if slot_list == egg_list:
        # spawn_egg特有の整形
        return item_id.split(":")[1].replace("_spawn_egg", "").replace("_", " ").title()
    elif slot_list == block_list:
        # ブロックは単純に名前部分だけ
        return item_id.split(":")[1].replace("_", " ").title()
    elif slot_list == plushie_list:
        # plushieなら名前を少し装飾
        return item_id.split(":")[1].replace("plushie_", "").replace("_", " ").title() + " Plushie"
    else:
        # デフォルト
        return item_id

# === Update subtitle ===
def update_subtitle(final=False):
    m.execute('title @a clear')

    names = [format_name(b) if b else "???" for b in results]
    text = " + ".join(names)

    m.execute('title @a title {"text":" ", "color":"white"}')
    m.execute(f'title @a subtitle {{"text":"{text}", "color":"aqua"}}')

    if final:
        time.sleep(0.4)  # 演出タイミングの調整

        if len(set(results)) == 1 and results[0] != "":
            jackpot_name = format_name(results[0])
            m.execute(f'title @a title {{"text":"🎉 JACKPOT! {jackpot_name}! 🎉", "color":"gold", "bold":true}}')

            # 演出サンプル（必要ならコメント解除）
            # m.execute('playsound minecraft:entity.player.levelup master @a')
            # m.execute('particle minecraft:firework ~ ~2 ~ 0.5 1 0.5 0.01 50')

# === Run one spin ===
def run_once():
    global rolling, stop_flag, results
    stop_flag = False
    rolling = [True, True, True]
    results = ["", "", ""]

    positions, facing = get_frame_positions_and_facing()
    setup_item_frames(positions, facing)

    m.echo("🎰 Slots are rolling! Press Enter to stop each slot!")

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

# === Main loop ===
def main():
    global stop_flag
    m.echo("🎮 Block Slot Machine Started!")
    m.echo("💬 Press Enter to stop each slot. Type 'stop' in chat to end.")

    while True:
        run_once()
        m.echo("🕹️ Type 'stop' in chat to end the round, or press Enter to restart.")

        stop_flag = False
        with m.EventQueue() as eq:
            eq.register_key_listener()
            eq.register_chat_listener()
            while True:
                event = eq.get()
                if event.type == m.EventType.CHAT and "stop" in event.message.lower():
                    stop_flag = True
                    m.echo("🛑 'stop' received. Exiting...")
                    return
                if event.type == m.EventType.KEY and event.action == 0 and event.key == 257:
                    break

main()
