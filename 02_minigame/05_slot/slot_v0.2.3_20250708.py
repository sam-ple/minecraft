import minescript as m
import time
from threading import Thread

# Spawn Egg Slot Machine with Item Frames 
# Uses **spawn eggs** shown in item frames that spin and stop.
# Item frames spin through different spawn eggs
# Stops each with Enter
# Displays current result in subtitle
# Shows JACKPOT title if all match

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

# === Get positions and facing for 3 item frames in a row in front of the player ===
def get_frame_positions_and_facing():
    x, y, z = m.player_position()
    yaw, _ = m.player_orientation()
    x, y, z = int(x), int(y), int(z)

    # Facing direction and alignment of item frames (aligned along X or Z axis)
    if 45 <= yaw < 135:      # West
        facing = 1  # west facing (item frames need reversed facing)
        positions = [(x-1, y+1, z-1), (x-1, y+1, z), (x-1, y+1, z+1)]
    elif 135 <= yaw < 225:   # North
        facing = 3  # south
        positions = [(x-1, y+1, z-1), (x, y+1, z-1), (x+1, y+1, z-1)]
    elif 225 <= yaw < 315:   # East
        facing = 0  # east
        positions = [(x+1, y+1, z+1), (x+1, y+1, z), (x+1, y+1, z-1)]
    else:                    # South (default)
        facing = 2  # north
        positions = [(x+1, y+1, z+1), (x, y+1, z+1), (x-1, y+1, z+1)]

    return positions, facing

# === Summon invisible item frame (transparent + fixed facing + spawn egg display) ===
def summon_invisible_item_frame(pos, facing, egg_id):
    x, y, z = pos
    # Remove nearby item frames (remove old frames at the same position)
    m.execute(f"kill @e[type=item_frame,x={x},y={y},z={z},distance=..1]")

    # Summon item frame with invisibility and fixed facing. Invisible:1b makes it invisible, Fixed:1b prevents rotation
    m.execute(
        f'summon item_frame {x} {y} {z} '
        f'{{Facing:{facing},Item:{{id:"{egg_id}",Count:1}},Invisible:1b,Fixed:1b}}'
    )

# === Roll one slot ===
def roll_slot(index, positions, facing):
    idx = 0
    while rolling[index] and not stop_flag:
        egg_id = egg_list[idx % len(egg_list)]
        summon_invisible_item_frame(positions[index], facing, egg_id)
        results[index] = egg_id  # Always save currently displayed item while rolling
        idx += 1
        time.sleep(0.2)

# === Update subtitle ===
def update_subtitle(final=False):
    names = []
    for b in results:
        if b and ":" in b:
            name = b.split(":")[1].replace("_spawn_egg", "").replace("_", " ").title()
            names.append(name)
        else:
            names.append("???")
    text = " + ".join(names)

    # First send empty title (so subtitle will show properly)
    m.execute('title @a title {"text":" ", "color":"white"}')
    m.execute(f'title @a subtitle {{"text":"{text}", "color":"aqua"}}')

    # On final slot stop only, show JACKPOT if all match
    if final and len(set(results)) == 1 and results[0] != "":
        time.sleep(0.2)  # Wait a little before showing JACKPOT (for effect)
        m.execute('title @a title {"text":"🎉 JACKPOT! 🎉", "color":"gold", "bold":true}')

# === Run one spin of the slots (3 slots) ===
def run_once():
    global rolling, stop_flag, results
    stop_flag = False
    rolling = [True, True, True]
    results = ["", "", ""]

    positions, facing = get_frame_positions_and_facing()

    m.echo("🎰 Slots are rolling! Press Enter to stop each slot!")

    # Start threads for each slot
    threads = []
    for i in range(3):
        t = Thread(target=roll_slot, args=(i, positions, facing), daemon=True)
        t.start()
        threads.append(t)

    # Stop each slot one by one by pressing Enter
    with m.EventQueue() as eq:
        eq.register_key_listener()
        idx = 0
        while idx < 3 and not stop_flag:
            event = eq.get()
            if event.type == m.EventType.KEY and event.action == 0 and event.key == 257:
                rolling[idx] = False
                time.sleep(0.3)  # Wait a bit for stop stabilization
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
                # If "stop" received in chat, set stop flag and exit
                if event.type == m.EventType.CHAT and "stop" in event.message.lower():
                    stop_flag = True
                    m.echo("🛑 'stop' received. Exiting...")
                    return
                # Restart on Enter key press
                if event.type == m.EventType.KEY and event.action == 0 and event.key == 257:
                    break

main()
