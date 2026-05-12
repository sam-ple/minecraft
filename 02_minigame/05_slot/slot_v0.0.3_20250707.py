import minescript as m
from minescript import EventQueue, EventType
import time
import random
from threading import Thread

# Add Title Display and Main Loop
# Adds a title showing current results. Allows multiple rounds.
# Chat command `"stop"` quits the game.
# Title shows live results (e.g., "Creeper + Spider + Enderman")
# Press Enter 3 times per round
# Multiple rounds until you type `"stop"` in chat

# === Settings ===
spawn_eggs = [
    "minecraft:zombie_spawn_egg",
    "minecraft:skeleton_spawn_egg",
    "minecraft:creeper_spawn_egg",
    "minecraft:spider_spawn_egg",
    "minecraft:enderman_spawn_egg"
]

rolling = [False, False, False]
results = ["", "", ""]
stop_flag = False

# === Slot rolling thread ===
def roll_egg_for_slot(index):
    while rolling[index] and not stop_flag:
        egg = random.choice(spawn_eggs)
        results[index] = egg
        m.execute(f"/item replace entity @p hotbar.{index} with {egg}")
        time.sleep(0.2)

# === Convert result names for display ===
def format_result_names():
    return [r.split(":")[1].replace("_spawn_egg", "").title() for r in results if r]

# === Update title with current result ===
def update_subtitle():
    names = format_result_names()
    joined = " + ".join(names)
    m.execute('title @a title {"text":""}')
    m.execute(f'title @a subtitle {{"text":"{joined}", "color":"aqua"}}')

# === Listen for stop command in chat ===
def listen_stop_command():
    global stop_flag
    with EventQueue() as eq:
        eq.register_chat_listener()
        while True:
            event = eq.get()
            if event.type == EventType.CHAT and "stop" in event.message.lower():
                stop_flag = True
                m.echo("🛑 Stop command received.")
                break

# === Play one round ===
def run_slot_machine_once():
    global rolling, results
    rolling = [True, False, False]
    results = ["", "", ""]

    m.echo("🎰 Slot 1 is rolling... Press Enter!")
    Thread(target=roll_egg_for_slot, args=(0,), daemon=True).start()

    with EventQueue() as eq:
        eq.register_key_listener()
        index = 0

        while index < 3 and not stop_flag:
            event = eq.get()
            if event.type == EventType.KEY and event.action == 0 and event.key == 257:
                rolling[index] = False
                m.echo(f"✅ Slot {index + 1} fixed: {results[index]}")
                update_subtitle()
                index += 1

                if index < 3 and not stop_flag:
                    rolling[index] = True
                    m.echo(f"🎰 Slot {index + 1} is rolling... Press Enter!")
                    Thread(target=roll_egg_for_slot, args=(index,), daemon=True).start()

        m.echo("🎉 Round finished!")
        m.echo(f"🎯 Result: {', '.join(format_result_names())}")

# === Main loop ===
def main_loop():
    global stop_flag
    m.echo("🎮 Slot machine started. Press Enter to stop each slot.")
    m.echo("💬 Type 'stop' in chat to quit.")
    Thread(target=listen_stop_command, daemon=True).start()

    while not stop_flag:
        run_slot_machine_once()
        time.sleep(2)

    m.echo("👋 Slot machine stopped.")

# === Start game ===
main_loop()
