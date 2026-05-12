import minescript as m
from minescript import EventQueue, EventType
import time
import random
from threading import Thread

# 3-Slot Machine with Sequential Stop
# Adds 3 independent slots that stop one-by-one when Enter is pressed.
# 3 hotbar slots
# Each stops with Enter key
# Final result shown in chat

# === Settings ===
spawn_eggs = [
    "minecraft:zombie_spawn_egg",
    "minecraft:skeleton_spawn_egg",
    "minecraft:creeper_spawn_egg",
    "minecraft:spider_spawn_egg",
    "minecraft:enderman_spawn_egg"
]

rolling = [True, False, False]
results = ["", "", ""]

def roll_egg_for_slot(slot_index):
    while rolling[slot_index]:
        egg = random.choice(spawn_eggs)
        results[slot_index] = egg
        m.execute(f"/item replace entity @p hotbar.{slot_index} with {egg}")
        time.sleep(0.2)

def listen_enter():
    with EventQueue() as eq:
        eq.register_key_listener()
        slot_index = 0
        m.echo("🎰 Slot 1 is rolling... Press Enter!")

        Thread(target=roll_egg_for_slot, args=(slot_index,), daemon=True).start()

        while slot_index < 3:
            event = eq.get()
            if event.type == EventType.KEY and event.action == 0 and event.key == 257:
                rolling[slot_index] = False
                m.echo(f"✅ Slot {slot_index + 1} fixed: {results[slot_index]}")
                slot_index += 1

                if slot_index < 3:
                    m.echo(f"🎰 Slot {slot_index + 1} is rolling... Press Enter!")
                    rolling[slot_index] = True
                    Thread(target=roll_egg_for_slot, args=(slot_index,), daemon=True).start()

        m.echo("🎉 All slots fixed!")
        m.echo(f"🎯 Final: {', '.join(results)}")

# === Run ===
listen_enter()
