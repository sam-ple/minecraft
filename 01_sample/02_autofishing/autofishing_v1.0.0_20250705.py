import minescript as m
import time
from threading import Thread

stop_flag = False
yaw_angle = 0.0
catch_counts = {}
triggered = False
start_time = time.time()

def listen_chat():
    global stop_flag
    with m.EventQueue() as eq:
        eq.register_chat_listener()
        while True:
            event = eq.get()
            if event.type == m.EventType.CHAT:
                msg = event.message.lower()
                if "stop" in msg:
                    m.echo("Stop command received. Stopping auto fishing.")
                    stop_flag = True
                    break

Thread(target=listen_chat, daemon=True).start()

def give_best_rod():
    m.execute('/item replace entity @p hotbar.0 with minecraft:fishing_rod')
    enchantments = [
        "minecraft:luck_of_the_sea 3",
        "minecraft:lure 3",
        "minecraft:unbreaking 3",
        "minecraft:mending 1"
    ]
    for ench in enchantments:
        m.execute(f"/enchant @p {ench}")

give_best_rod()

def rotate_view():
    global yaw_angle
    _, pitch = m.player_orientation()
    yaw_angle += 45.0
    if yaw_angle >= 360.0:
        yaw_angle -= 360.0
    m.player_set_orientation(yaw_angle, pitch)

def find_bobber():
    for entity in m.entities():
        if "fishing_bobber" in entity.type.lower():
            return entity
    return None

def wait_for_bite(bobber, timeout=30):
    start = time.time()
    last_y = bobber.position[1]
    while time.time() - start < timeout:
        if stop_flag:
            return False
        entity = find_bobber()
        if entity:
            y = entity.position[1]
            if y - last_y > 0.2:
                return True
            last_y = y
        time.sleep(0.1)
    return False

def snapshot_inventory():
    inv = m.player_inventory()
    return {item.item: item.count for item in inv if item.count > 0}

def detect_catch(before, after):
    for item, count in after.items():
        if item not in before:
            return item
        elif count > before[item]:
            return item
    return None

def lap_time():
    elapsed = time.time() - start_time
    mins = int(elapsed // 60)
    secs = int(elapsed % 60)
    return f"{mins:02}:{secs:02}"

def print_catch_summary():
    m.echo("----- Catch Summary -----")
    for name, count in catch_counts.items():
        m.echo(f" - {name}: {count} times")
    m.echo(f"Elapsed Time: {lap_time()}")

def save_summary_to_file():
    filename = f"summary_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("---- Catch Summary ----\n")
        for name, count in catch_counts.items():
            f.write(f" - {name}: {count} times\n")
        f.write(f"Elapsed Time: {lap_time()}\n")
    m.echo(f"Summary saved to: {filename}")

def handle_inventory_full():
    global triggered
    inv = m.player_inventory()
    slots_used = len(inv)

    if slots_used >= 36 and not triggered:
        triggered = True

        # Open chat and display summary
        m.show_chat_screen(True, "")
        time.sleep(0.5)
        print_catch_summary()
        time.sleep(1)

        # Take a screenshot
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"autofish_{timestamp}.png"
        m.screenshot(filename)
        m.echo(f"Screenshot saved: {filename}")

        # Save summary to text file
        save_summary_to_file()

        time.sleep(2)
        m.show_chat_screen(False)

        # Clear inventory
        m.execute("/clear @p")
        m.echo("Inventory cleared.")

        # Restore fishing rod
        give_best_rod()
        m.echo("Rod restored.")

    elif slots_used < 36:
        triggered = False

# Initial message and time display
m.echo("Auto fishing started.")
m.echo(f"Start Time: {lap_time()}")

# Main loop
while not stop_flag:
    rotate_view()
    handle_inventory_full()

    before = snapshot_inventory()

    m.player_press_use(True)
    m.player_press_use(False)
    time.sleep(2)

    bobber = find_bobber()
    if bobber and wait_for_bite(bobber):
        m.player_press_use(True)
        m.player_press_use(False)
        time.sleep(1)

        after = snapshot_inventory()
        item_name = detect_catch(before, after)

        if item_name:
            catch_counts[item_name] = catch_counts.get(item_name, 0) + 1
            m.echo(f"Caught: {item_name}  (Total: {catch_counts[item_name]})")
            m.echo(f"Lap Time: {lap_time()}")
        else:
            m.echo("Fish caught, but item not detected.")
    else:
        m.echo("No bite.")

    time.sleep(1)

# Final process
m.echo("Auto fishing stopped.")
print_catch_summary()
save_summary_to_file()
