import minescript as m
import time
from threading import Thread

# Block Slot Machine (1 block in front)
# Spins **blocks** like ores in front of the player using `/setblock`.
# Displays ore blocks in front of player
# Stops with Enter key
# Shows JACKPOT if 3 match

# === Settings ===
block_list = [
    "minecraft:iron_ore",
    "minecraft:gold_ore",
    "minecraft:diamond_ore",
    "minecraft:copper_ore",
    "minecraft:coal_ore",
    "minecraft:lapis_ore"
]

rolling = False
stop_flag = False

# === Get slot position (2 blocks in front of player) ===
def get_slot_pos():
    x, y, z = m.player_position()
    yaw, _ = m.player_orientation()
    x, y, z = int(x), int(y), int(z)

    if 45 <= yaw < 135:
        return (x-2, y+1, z)  # West
    elif 135 <= yaw < 225:
        return (x, y+1, z-2)  # North
    elif 225 <= yaw < 315:
        return (x+2, y+1, z)  # East
    else:
        return (x, y+1, z+2)  # South (default)

# === Rolling animation using setblock ===
def roll():
    global rolling
    pos = get_slot_pos()
    idx = 0
    while rolling and not stop_flag:
        block = block_list[idx % len(block_list)]
        x, y, z = pos
        m.execute(f"setblock {x} {y-1} {z} minecraft:stone")
        m.execute(f"setblock {x} {y} {z} minecraft:air")
        m.execute(f"setblock {x} {y} {z} {block}")
        idx += 1
        time.sleep(0.2)

# === Main execution ===
def main():
    global rolling, stop_flag
    stop_flag = False
    rolling = True

    m.echo("🎰 Rolling... Press Enter to stop!")

    Thread(target=roll, daemon=True).start()

    with m.EventQueue() as eq:
        eq.register_key_listener()
        while True:
            event = eq.get()
            if event.type == m.EventType.KEY and event.action == 0 and event.key == 257:
                rolling = False
                m.echo("🛑 Stopped!")
                break

main()
