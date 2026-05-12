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
        m.execute(
            f'summon item_frame {x} {y} {z} '
            f'{{Facing:{facing},Item:{{id:"{egg_list[0]}",Count:1}},Invisible:1b,Fixed:1b,Tags:["slot_{i}"]}}'
        )

# === Update content only (lightweight) ===
def update_item_frame(index, egg_id):
    m.execute(
        f'data modify entity @e[type=item_frame,tag=slot_{index},limit=1,sort=nearest] '
        f'Item set value {{id:"{egg_id}",Count:1b}}'
    )

# === Roll one slot ===
def roll_slot(index):
    idx = 0
    while rolling[index] and not stop_flag:
        egg_id = egg_list[idx % len(egg_list)]
        update_item_frame(index, egg_id)
        results[index] = egg_id
        idx += 1
        time.sleep(0.2)
    # スロット停止時の効果音
    m.execute('playsound minecraft:block.note_block.hat master @a')

# === Update subtitle ===
def update_subtitle(final=False):
    # 画面のタイトルを一度クリア（前の表示が残らないように）
    m.execute('title @a clear')

    names = []
    for b in results:
        if b and ":" in b:
            name = b.split(":")[1].replace("_spawn_egg", "").replace("_", " ").title()
            names.append(name)
        else:
            names.append("???")
    
    # スロットの結果（例：Cow + Pig + Cow）を文字列に
    text = " + ".join(names)

    # 空のタイトルと、サブタイトルに結果表示
    m.execute('title @a title {"text":" ", "color":"white"}')
    m.execute(f'title @a subtitle {{"text":"{text}", "color":"aqua"}}')

    # JACKPOT 条件：3つすべて同じ、かつ空でない
    if final:
        time.sleep(0.4)  # アニメーションタイミングを揃えるための少しの遅延

        if len(set(results)) == 1 and results[0] != "":
            mob_name = results[0].split(":")[1].replace("_spawn_egg", "").replace("_", " ").title()
            m.execute(f'title @a title {{"text":"🎉 JACKPOT! {mob_name}! 🎉", "color":"gold", "bold":true}}')

            # 音やパーティクル演出を追加したい場合：
            m.execute('playsound minecraft:entity.player.levelup master @a')
            m.execute('particle minecraft:firework ~ ~2 ~ 0.5 1 0.5 0.01 50')

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