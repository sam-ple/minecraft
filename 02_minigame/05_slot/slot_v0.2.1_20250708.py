import minescript as m
import time
from threading import Thread

# 3-Slot Block Machine
# Spins 3 ore blocks side-by-side in front of the player.
# Spins 3 slots with blocks like iron/gold/diamond ore
# Stops each slot with Enter key
# Title and subtitle show JACKPOT if all match

# === Settings ===
block_list = [
    "minecraft:iron_ore",
    "minecraft:gold_ore",
    "minecraft:diamond_ore",
    "minecraft:copper_ore",
    "minecraft:coal_ore",
    "minecraft:lapis_ore"
]

rolling = [False, False, False]
stop_flag = False
results = ["", "", ""]

# === Get 3 slot positions in front of the player ===
def get_slot_positions():
    x, y, z = m.player_position()
    yaw, _ = m.player_orientation()
    x, y, z = int(x), int(y), int(z)

    if 45 <= yaw < 135:
        return [(x-2, y+1, z+i) for i in [-1, 0, 1]]
    elif 135 <= yaw < 225:
        return [(x+i, y+1, z-2) for i in [-1, 0, 1]]
    elif 225 <= yaw < 315:
        return [(x+2, y+1, z+i) for i in [-1, 0, 1]]
    else:
        return [(x+i, y+1, z+2) for i in [-1, 0, 1]]

# === Individual slot rolling animation ===
def roll_slot(index):
    pos = get_slot_positions()[index]
    idx = 0
    while rolling[index] and not stop_flag:
        block = block_list[idx % len(block_list)]
        results[index] = block
        x, y, z = pos
        m.execute(f"setblock {x} {y-1} {z} minecraft:stone")
        m.execute(f"setblock {x} {y} {z} minecraft:air")
        m.execute(f"setblock {x} {y} {z} {block}")
        idx += 1
        time.sleep(0.2)

# === Main execution ===
def main():
    global rolling, stop_flag, results
    stop_flag = False
    rolling = [True, False, False]
    results = ["", "", ""]

    m.echo("🎰 Slot 1 is spinning... Press Enter to stop!")

    Thread(target=roll_slot, args=(0,), daemon=True).start()

    with m.EventQueue() as eq:
        eq.register_key_listener()
        index = 0
        while index < 3 and not stop_flag:
            event = eq.get()
            if event.type == m.EventType.KEY and event.action == 0 and event.key == 257:
                rolling[index] = False
                m.echo(f"✅ Slot {index+1} stopped: {results[index]}")
                index += 1
                if index < 3:
                    rolling[index] = True
                    m.echo(f"🎰 Slot {index+1} is spinning... Press Enter to stop!")
                    Thread(target=roll_slot, args=(index,), daemon=True).start()

    # === Result check ===
    if results[0] and results[0] == results[1] == results[2]:
        name = results[0].split(":")[1].replace("_ore", "").title()
        m.execute(f'title @a title {{"text":"JACKPOT!", "color":"gold", "bold":true}}')
        m.execute(f'title @a subtitle {{"text":"{name} x3!", "color":"aqua"}}')

    m.echo("🕹️ Press Enter to play again.")

main()
