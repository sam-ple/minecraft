import minescript as m
from minescript import EventQueue, EventType
import time
import random
from threading import Thread

# Add JACKPOT Effect
# Adds a **JACKPOT title** and sound effect if all 3 slots match.
# Checks if all 3 slots match
# Adds fancy title and sound effect

# === Configuration ===
spawn_eggs = [
    "minecraft:zombie_spawn_egg",
    "minecraft:skeleton_spawn_egg",
    "minecraft:creeper_spawn_egg",
    "minecraft:spider_spawn_egg",
    "minecraft:enderman_spawn_egg"
]

# === Game state ===
rolling = [False, False, False]
results = ["", "", ""]
stop_flag = False

# === Roll one slot ===
def roll_egg_for_slot(index):
    while rolling[index] and not stop_flag:
        egg = random.choice(spawn_eggs)
        results[index] = egg
        m.execute(f"/item replace entity @p hotbar.{index} with {egg}")
        time.sleep(0.2)

# === Format display names (e.g. "Creeper") ===
def format_result_names():
    return [r.split(":")[1].replace("_spawn_egg", "").title() for r in results if r]

# === Show subtitle with current result ===
def update_subtitle():
    names = format_result_names()
    joined = " + ".join(names)
    m.execute('title @a title {"text":""}')  # Required to show subtitle
    m.execute(f'title @a subtitle {{"text":"{joined}", "color":"aqua"}}')

# === Listen to chat "stop" ===
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

# === Check for 3-matching JACKPOT ===
def check_and_celebrate_if_matched():
    if results[0] and results[0] == results[1] == results[2]:
        name = format_result_names()[0]
        m.execute(f'title @a title {{"text":"JACKPOT!", "color":"gold", "bold":true}}')
        m.execute(f'title @a subtitle {{"text":"{name} x3!!", "color":"light_purple"}}')
        m.execute('playsound minecraft:entity.experience_orb.pickup master @a ~ ~ ~ 1 2')
        m.execute('playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1')

# === Run one round ===
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
        check_and_celebrate_if_matched()

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

# === Run the game ===
main_loop()
