import minescript as m
import time
import math
import threading
from minescript import EventQueue, EventType

running = False

def place_tnt_loop():
    global running
    while running:
        x, y, z = m.player_position()
        x, y, z = math.floor(x), math.floor(y), math.floor(z)

        block_below = m.getblock(x, y-1, z)

        TARGET_BLOCKS = ["minecraft:dirt", "minecraft:grass_block"]
        if any(target in block_below for target in TARGET_BLOCKS):
            m.execute(f"setblock {x} {y-1} {z} minecraft:tnt")
            m.echo(f"TNT placed underfoot at {x},{y-1},{z}")

        time.sleep(0.1)

def main():
    global running
    with EventQueue() as eq:
        eq.register_chat_listener()
        while True:
            event = eq.get()
            if event.type == EventType.CHAT:
                msg = event.message.strip()
                if msg == "--start" and not running:
                    running = True
                    threading.Thread(target=place_tnt_loop, daemon=True).start()
                    m.echo("TNT underfoot started!")
                elif msg == "--stop":
                    running = False
                    m.echo("TNT underfoot stopped.")

if __name__ == "__main__":
    m.echo("TNT underfoot ready! Use --start and --stop in chat.")
    main()
