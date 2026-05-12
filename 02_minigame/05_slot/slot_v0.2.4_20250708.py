import minescript as m
import time
from threading import Thread

# Plushie Slot Machine (Plushie Buddies) 
# Uses items like `plushie_buddies:plushie_breeze` in invisible item frames.
# Spins cute plushies in invisible item frames
# Stops each with Enter
# Subtitle shows plushie names
# JACKPOT message if all match

# === Settings (List of plushie item IDs) ===
plushie_list = [
    "plushie_buddies:plushie_breeze",
    "plushie_buddies:plushie_sniffer",
    "plushie_buddies:plushie_allay"
]

rolling = [False, False, False]
stop_flag = False
results = ["", "", ""]

# === Get positions and facing for 3 item frames in front of player ===
def get_frame_positions_and_facing():
    x, y, z = m.player_position()
    yaw, _ = m.player_orientation()
    x, y, z = int(x), int(y), int(z)

    if 45 <= yaw < 135:      # Facing West
        facing = 1  # west
        positions = [(x-1, y+1, z-1), (x-1, y+1, z), (x-1, y+1, z+1)]
    elif 135 <= yaw < 225:   # Facing North
        facing = 3  # south
        positions = [(x-1, y+1, z-1), (x, y+1, z-1), (x+1, y+1, z-1)]
    elif 225 <= yaw < 315:   # Facing East
        facing = 0  # east
        positions = [(x+1, y+1, z+1), (x+1, y+1, z), (x+1, y+1, z-1)]
    else:                    # Facing South (default)
        facing = 2  # north
        positions = [(x+1, y+1, z+1), (x, y+1, z+1), (x-1, y+1, z+1)]

    return positions, facing

# === Summon transparent, fixed-facing item frame displaying a plushie ===
def summon_invisible_item_frame(pos, facing, item_id):
    x, y, z = pos
    # Kill any existing item frames at exact position
    m.execute(f"kill @e[type=item_frame,x={x},y={y},z={z},dx=0,dy=0,dz=0]")

    m.execute(
        f'summon item_frame {x} {y} {z} '
        f'{{Facing:{facing},Item:{{id:"{item_id}",Count:1}},Invisible:1b,Fixed:1b}}'
    )

# === Roll one slot until stopped ===
def roll_slot(index, positions, facing):
    idx = 0
    while rolling[index] and not stop_flag:
        item_id = plushie_list[idx % len(plushie_list)]
        summon_invisible_item_frame(positions[index], facing, item_id)
        results[index] = item_id
        idx += 1
        time.sleep(0.2)

# === Update subtitle to show current plushies ===
def update_subtitle(final=False):
    names = []
    for item in results:
        if item and ":" in item:
            name = item.split(":")[1].replace("plushie_", "").replace("_", " ").title()
            names.append(name)
        else:
            names.append("???")
    text = " + ".join(names)

    # Clear title so subtitle shows properly
    m.execute('title @a title {"text":" ", "color":"white"}')
    m.execute(f'title @a subtitle {{"text":"{text}", "color":"aqua"}}')

    # Show JACKPOT if all plushies match
    if final and len(set(results)) == 1 and results[0] != "":
        time.sleep(0.2)
        m.execute('title @a title {"text":"🎉 JACKPOT! 🎉", "color":"gold", "bold":true}')

# === Run one round of 3-slot plushie machine ===
def run_once():
    global rolling, stop_flag, results
    stop_flag = False
    rolling = [True, True, True]
    results = ["", "", ""]

    positions, facing = get_frame_positions_and_facing()

    # Start threads for rolling slots
    threads = []
    for i in range(3):
        t = Thread(target=roll_slot, args=(i, positions, facing), daemon=True)
        t.start()
        threads.append(t)

    # Wait for Enter to stop each slot in order
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

# === Main game loop ===
def main():
    global stop_flag
    m.echo("🎮 Plushie Slot Machine Started!")
    m.echo("💬 Press Enter to stop each slot. Type 'stop' in chat to quit.")

    while True:
        run_once()
        m.echo("🕹️ Press Enter to play again. Type 'stop' to quit.")

        stop_flag = False
        with m.EventQueue() as eq:
            eq.register_key_listener()
            eq.register_chat_listener()
            while True:
                event = eq.get()
                if event.type == m.EventType.CHAT and "stop" in event.message.lower():
                    stop_flag = True
                    m.echo("🛑 Exiting...")
                    return
                if event.type == m.EventType.KEY and event.action == 0 and event.key == 257:
                    break

main()
