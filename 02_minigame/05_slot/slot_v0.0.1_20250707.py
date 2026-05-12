import minescript as m
from minescript import EventQueue, EventType
import time
import random
from threading import Thread

# Basic 1-Slot Machine
# A single hotbar slot spins spawn eggs until Enter is pressed.
# Spins only 1 slot
# Stops when Enter is pressed
# Displays final result in chat

# === Settings ===
spawn_eggs = [
    "minecraft:zombie_spawn_egg",
    "minecraft:skeleton_spawn_egg",
    "minecraft:creeper_spawn_egg",
    "minecraft:spider_spawn_egg",
    "minecraft:enderman_spawn_egg"
]
HOTBAR_SLOT = 0
rolling = True
current_egg = spawn_eggs[0]

# === Rolling thread ===
def roll_eggs():
    global current_egg, rolling
    while rolling:
        current_egg = random.choice(spawn_eggs)
        m.execute(f"/item replace entity @p hotbar.{HOTBAR_SLOT} with {current_egg}")
        time.sleep(0.2)

# === Listen for Enter key ===
def listen_enter():
    global rolling
    with EventQueue() as eq:
        eq.register_key_listener()
        while True:
            event = eq.get()
            if event.type == EventType.KEY and event.action == 0 and event.key == 257:
                rolling = False
                m.echo(f"You got: {current_egg}")
                break

# === Run ===
m.echo("🎰 Slot is rolling... Press Enter to stop!")
Thread(target=roll_eggs, daemon=True).start()
listen_enter()
