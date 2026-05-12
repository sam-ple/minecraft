# 🧪 Minescript Basics – Expanded Tutorial Series

A continuation of the Minescript beginner tutorials. These steps introduce player control, interaction, inventory inspection, event handling, and entity actions.

---

* Written by crocado
* Environment: Minescript 4.0 / Fabric 1.21.5 @ Modrinth   
* Recommended environment: local creative world  
* 📄 Please review the [Minescript Terms of Use](https://github.com/maxuser0/minescript/blob/main/TERMS_OF_USE.md) to ensure that your usage is compliant.

---

#### 🎥 YouTube

* [{ Minescript Tutorial #2 } Basic Player Controls and Auto Actions](https://www.youtube.com/watch?v=1n3pcL5cj-4)  
  
---

### 📘 Tutorial 8 – Move and Jump

A simple movement demo: simulate pressing the forward key and then jump.

##### `player.press_forward()`

Simulates the player holding down the **forward (W)** key.  
This function keeps the player moving forward until `player.release_forward()` is called.  
https://minescript.net/docs/#player_press_forward  

##### `player.press_jump()`

Simulates the player holding down the **jump (space)** key.  
The player will continue jumping until `player.release_jump()` is called.  
https://minescript.net/docs/#player_press_jump  


```python
import minescript as m
import time

# Move forward briefly
m.player_press_forward(True)
time.sleep(0.5)
m.player_press_forward(False)

# Jump
m.player_press_jump(True)
time.sleep(0.2)
m.player_press_jump(False)
```

---

### 📘 Tutorial 9 – Look Forward and Get Target Block

Set the player's orientation and detect the block being targeted.

##### `player.get_targeted_block()`

Returns information about the block the player is currently looking at.  
Useful for detecting interactions with the environment.  
https://minescript.net/docs/#player_get_targeted_block  


```python
import minescript as m

# Face forward
# m.player_set_orientation(0, 0)

# Get the targeted block
block = m.player_get_targeted_block(10)
if block:
    m.echo(f"Target Block: {block.type} @ {block.position}")
else:
    m.echo("No block in crosshairs")
```

---

### 📘 Tutorial 10 – Right Click to Use Item

Right-click (use) the block in front of the player.

##### `player.look_at(x, y, z)`

Turns the player's view to face the specified coordinates.  
Helpful for aiming or orienting toward specific targets.  
https://minescript.net/docs/#player_look_at  

##### `player.press_use()`

Simulates pressing the **use (right-click)** key.  
This can be used for interacting with blocks, entities, or items.  
https://minescript.net/docs/#player_press_use  

```python
import minescript as m
import time

# Give oak sapling to main hand
m.execute("/item replace entity @p hotbar.0 with minecraft:oak_sapling")

# Get current player position
x, y, z = m.player_position()
# Look at the ground 3 blocks ahead
m.player_look_at(x, y - 1, z + 3)

# Right-click to use (try to plant the sapling)
m.player_press_use(True)
time.sleep(0.2)
m.player_press_use(False)
```

---

### 📘 Tutorial 11 – Check Hand Items and Inventory

View what the player is holding and what's in their inventory.

##### `player.hand_items()`

Returns a tuple with the items currently held in the player's main and off hands.  
Useful for checking what the player is holding before performing actions.  
https://minescript.net/docs/#player_hand_items  

##### `player.inventory()`

Returns a list of items in the player's inventory.  
Allows inspection or processing of inventory contents.  
https://minescript.net/docs/#player_inventory  

```python
import minescript as m

m.execute('/item replace entity @p weapon.mainhand with minecraft:diamond_sword')
m.execute('/item replace entity @p armor.head with minecraft:diamond_helmet')
m.execute('/item replace entity @p armor.chest with minecraft:diamond_chestplate')
m.execute('/item replace entity @p armor.legs with minecraft:diamond_leggings')
m.execute('/item replace entity @p armor.feet with minecraft:diamond_boots')
m.execute('/item replace entity @p weapon.offhand with minecraft:shield')
m.execute('/item replace entity @p hotbar.1 with minecraft:oak_sapling 6')
m.execute('/item replace entity @p hotbar.2 with minecraft:carrot 10')
m.execute('/item replace entity @p hotbar.3 with minecraft:iron_sword 1')
m.execute('/item replace entity @p hotbar.4 with minecraft:bread 3')

# Check items in both hands
hands = m.player_hand_items()
m.echo(f"Main hand: {hands.main_hand.item}")
m.echo(f"Off hand: {hands.off_hand.item}")

# Show inventory items
for item in m.player_inventory():
    m.echo(f"Slot {item.slot}: {item.item} x{item.count}")
```

---

### 📘 Tutorial 12 – React to Chat Event

React to specific messages typed in chat (e.g., jump when player types “sample”).

##### `register_chat_listener()`

Registers a listener to detect when players send chat messages.  
Used for triggering actions based on chat input.  
https://minescript.net/docs/#register_chat_listener  

```python
import minescript as m
import time

with m.EventQueue() as events:
    events.register_chat_listener()
    m.echo("Type 's a m p l e' in chat to jump! Please remove the spaces.")

    while True:
        event = events.get()
        if event.type == m.EventType.CHAT and "sample" in event.message.lower():
            m.echo("Jumping!")
            m.player_press_jump(True)
            time.sleep(0.3)
            m.player_press_jump(False)

# Using "jump" would cause continuous jumping,
# so I use "sample" instead. 
# There are ways to avoid this, but they make the code longer,
# so I keep it simple here. 
# Considering future tutorials to improve this code step-by-step.

```

---

### 📘 Tutorial 13 – Auto Walk and Interact

Auto-walk forward while periodically using the item in hand.

```python
import minescript as m
import time

m.execute('/give @p minecraft:sweet_berries 64')

m.echo("Auto walking started")

while True:
    m.player_press_forward(True)
    m.player_press_use(True)
    time.sleep(0.2)
    m.player_press_use(False)
    time.sleep(1)

# This will keep walking forever, so please stop it with "\killjob -1".
# There are ways to avoid this, but they make the code longer,
# so I keep it simple here. 
# Considering future tutorials to improve this code step-by-step.

```

---

### 📘 Tutorial 14 – Auto Fishing System

Cast a fishing rod, detect bobber movement, and reel in when there's a bite.

```python
import minescript as m
import time

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
        entity = find_bobber()
        if entity:
            y = entity.position[1]
            if y - last_y > 0.2:
                return True
            last_y = y
        time.sleep(0.1)
    return False

while True:
    m.player_press_use(True)
    m.player_press_use(False)
    time.sleep(2)

    bobber = find_bobber()
    if bobber and wait_for_bite(bobber):
        m.echo("Fish caught!")
        m.player_press_use(True)
        m.player_press_use(False)

    time.sleep(1)

# This will keep fishing forever, so please stop it with "\killjob -1".
# There are ways to avoid this, but they make the code longer,
# so I keep it simple here. 
# Considering future tutorials to improve this code step-by-step.

```
