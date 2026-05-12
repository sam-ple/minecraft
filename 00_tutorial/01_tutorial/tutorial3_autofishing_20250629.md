# 🧪 Minescript Basics – Expanded Tutorial Series  

"Tutorial 14 – Auto Fishing System" was originally endless and could not be stopped. This version adds a stop function and includes several improvements.

---

* Written by crocado
* Environment: Minescript 4.0 / Fabric 1.21.5 @ Modrinth   
* Recommended environment: local creative world  
* 📄 Please review the [Minescript Terms of Use](https://github.com/maxuser0/minescript/blob/main/TERMS_OF_USE.md) to ensure that your usage is compliant.

---

#### 🎥 YouTube

* [{ Minescript Tutorial #3 } Growing the Auto Fishing Script Step-by-Step in Minescript](https://www.youtube.com/watch?v=mAXT14GW_7w)  
  
---

### 📘 Tutorial 14-1 – Auto Fishing with Stop Command

An auto fishing script that listens for a chat "stop" command to end the fishing loop.

```python
import minescript as m
import time
from threading import Thread

stop_flag = False

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

m.execute('/item replace entity @p hotbar.0 with minecraft:fishing_rod')
map_enchants = [
    "minecraft:luck_of_the_sea 3",
    "minecraft:lure 3",
    "minecraft:unbreaking 3",
    "minecraft:mending 1"
]
for ench in map_enchants:
    m.execute(f"/enchant @p {ench}")

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

while True:
    if stop_flag:
        break

    m.player_press_use(True)
    m.player_press_use(False)
    time.sleep(2)

    bobber = find_bobber()
    if bobber and wait_for_bite(bobber):
        m.echo("Fish caught!")
        m.player_press_use(True)
        m.player_press_use(False)

    time.sleep(1)

m.echo("Auto fishing stopped.")
```

---

### 📘 Tutorial 14-2 – Auto Fishing with Rotating View

Adds a rotation of the player's view by 45 degrees each fishing cycle to simulate looking around.

```python
import minescript as m
import time
from threading import Thread

stop_flag = False
yaw_angle = 0.0  # Initial yaw angle

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

# Prepare fishing rod and enchantments
m.execute('/item replace entity @p hotbar.0 with minecraft:fishing_rod')
map_enchants = [
    "minecraft:luck_of_the_sea 3",
    "minecraft:lure 3",
    "minecraft:unbreaking 3",
    "minecraft:mending 1"
]
for ench in map_enchants:
    m.execute(f"/enchant @p {ench}")

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

def rotate_view():
    global yaw_angle
    _, pitch = m.player_orientation()
    yaw_angle += 45.0  # Rotate 45 degrees per cycle
    if yaw_angle >= 360.0:
        yaw_angle -= 360.0
    m.player_set_orientation(yaw_angle, pitch)

while not stop_flag:
    rotate_view()
    m.player_press_use(True)
    m.player_press_use(False)
    time.sleep(2)

    bobber = find_bobber()
    if bobber and wait_for_bite(bobber):
        m.echo("Fish caught!")
        m.player_press_use(True)
        m.player_press_use(False)

    time.sleep(1)

m.echo("Auto fishing stopped.")
```

---

### 📘 Tutorial 14-3 – Auto Fishing with Catch Count and Inventory Detection

Tracks and reports each type of caught item with totals displayed at the end.

```python
import minescript as m
import time
from threading import Thread

stop_flag = False
yaw_angle = 0.0  # Initial yaw angle
catch_counts = {}  # Dictionary to track catch counts by item type

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

# Prepare fishing rod and enchantments
m.execute('/item replace entity @p hotbar.0 with minecraft:fishing_rod')
map_enchants = [
    "minecraft:luck_of_the_sea 3",
    "minecraft:lure 3",
    "minecraft:unbreaking 3",
    "minecraft:mending 1"
]
for ench in map_enchants:
    m.execute(f"/enchant @p {ench}")

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

def rotate_view():
    global yaw_angle
    _, pitch = m.player_orientation()
    yaw_angle += 45.0
    if yaw_angle >= 360.0:
        yaw_angle -= 360.0
    m.player_set_orientation(yaw_angle, pitch)

def snapshot_inventory():
    inv = m.player_inventory()
    return {item.item: item.count for item in inv if item.count > 0}

def detect_catch(before, after):
    for item, count in after.items():
        if item not in before:
            return item, count
        elif count > before[item]:
            return item, count - before[item]
    return None, 0

while not stop_flag:
    rotate_view()

    before_items = snapshot_inventory()

    m.player_press_use(True)
    m.player_press_use(False)
    time.sleep(2)

    bobber = find_bobber()
    if bobber and wait_for_bite(bobber):
        m.player_press_use(True)
        m.player_press_use(False)
        time.sleep(1)  # Wait for drops to register

        after_items = snapshot_inventory()
        item_name, amount = detect_catch(before_items, after_items)

        if item_name:
            catch_counts[item_name] = catch_counts.get(item_name, 0) + amount
            m.echo(f"Caught: {item_name} ×{amount} (Total: {catch_counts[item_name]})")
        else:
            m.echo("Fish caught, but item not detected.")
    else:
        m.echo("No bite.")

    time.sleep(1)

m.echo("Auto fishing stopped.")
m.echo("Final Catch Summary:")
for name, count in catch_counts.items():
    m.echo(f" - {name}: {count} times")
```
