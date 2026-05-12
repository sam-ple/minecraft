# 🧪 Minescript Basics – Tutorial Series

This tutorial introduces the basics of using **Minescript** for Minecraft scripting. Each step builds on the last, showing how to get started with player position, echoing messages, teleportation, and using imports.

---

* Written by crocado  
* Environment: Minescript 4.0 / Fabric 1.21.5 @ Modrinth   
* Recommended environment: local creative world  
* 📄 Please review the [Minescript Terms of Use](https://github.com/maxuser0/minescript/blob/main/TERMS_OF_USE.md) to ensure that your usage is compliant.

---

#### 🎥 YouTube

* [{ Minescript Tutorial #1 } Introduction to Minescript: Basics and Simple Commands](https://www.youtube.com/watch?v=okaWf-2lkGU)  
  
---

### 📘 Tutorial 1 – Hello World

A simple script to verify that Minescript is working correctly.

##### `echo()`

Prints a message to the in-game chat.
Useful for debugging or providing feedback to the player.
[https://minescript.net/docs/#echo](https://minescript.net/docs/#echo)


```python
import minescript  # Import the minescript module

minescript.echo("Hello from Minescript!")  # Output a message to the Minecraft chat
```

---

### 📘 Tutorial 2 – Get Player Position

Get and print the player's current coordinates in the Minecraft world.

##### `player.position()`

Returns the player's current position as an `(x, y, z)` tuple.
This is useful for tracking movement or targeting actions.
[https://minescript.net/docs/#player\_position](https://minescript.net/docs/#player_position)

```python
import minescript

# Get the current player position (floats)
x, y, z = minescript.player_position()

# Convert to integers for clean display
x, y, z = int(x), int(y), int(z)

# Show the position in chat
minescript.echo(f"Current Position: X={x}, Y={y}, Z={z}")
```

---

### 📘 Tutorial 3 – Teleport Relative to Current Position

Move the player 3 blocks east and 3 blocks south, and rotate them to face directly south.

##### `execute(command: str)`

Executes a raw Minecraft command as if entered in the game.
Useful for advanced actions not directly supported by Minescript.
[https://minescript.net/docs/#execute](https://minescript.net/docs/#execute)

```python
import minescript

# Get and convert player position
x, y, z = minescript.player_position()
x, y, z = int(x), int(y), int(z)

minescript.echo(f"Current Position: X={x}, Y={y}, Z={z}")

# Teleport the player relative to current position and face south
minescript.execute(f"/tp @p {x+3} {y} {z+3} 0 0")
minescript.echo("Teleported to x+3, z+3 and faced due south.")
```

---

### 📘 Tutorial 4 – Wait, Then Teleport

Adds a short delay before teleporting the player.

```python
import time
import minescript

x, y, z = minescript.player_position()
x, y, z = int(x), int(y), int(z)
minescript.echo(f"Current Position: X={x}, Y={y}, Z={z}")

time.sleep(3)  # Wait for 3 seconds

minescript.execute(f"/tp @p {x+3} {y} {z+3} 0 0")
minescript.echo("Teleported after delay to x+3, z+3 and faced due south.")
```

---

### 📘 Tutorial 4a – Clean Import Style

Same as Tutorial 4 but using cleaner, explicit imports and built-in `map()`.

```python
from time import sleep
from minescript import player_position, echo, execute

# Get and convert position using map()
x, y, z = map(int, player_position())
echo(f"Current Position: X={x}, Y={y}, Z={z}")

sleep(3)  # Wait 3 seconds

execute(f"/tp @p {x+3} {y} {z+3} 0 0")
echo("Teleported after delay to x+3, z+3 and faced due south.")
```

---

### 📘 Tutorial 5 – Summon Mobs with Delay

Summon different mobs one after another near the player, with a short delay between each.

```python
from time import sleep
from minescript import player_position, echo, execute

# Get and convert player position
x, y, z = map(int, player_position())

# Summon an Allay at x+3, z+3
execute(f"/summon minecraft:allay {x+3} {y} {z+3} {{}}")
sleep(3)

# Summon a warm-variant cow (note: "variant" NBT works only in some versions/mods)
execute(f'/summon minecraft:cow {x+3} {y} {z+3} {{"variant":"warm"}}')
sleep(3)

# Summon a cold-variant chicken (same note as above)
execute(f'/summon minecraft:chicken {x+3} {y} {z+3} {{"variant":"cold"}}')
```

---

### 📘 Tutorial 6 – Circular Mob Summoning

Summon the same type of mob (Allay) in a circular pattern around the player.

```python
from time import sleep
import math
from minescript import player_position, echo, execute

x, y, z = map(int, player_position())

mob = "allay"
num_mobs = 12
radius = 1

for i in range(num_mobs):
    angle = 2 * math.pi * i / num_mobs
    dx = round(math.cos(angle) * radius, 2)
    dz = round(math.sin(angle) * radius, 2)
    sx = x + dx
    sy = y
    sz = z + dz
    execute(f'/summon minecraft:{mob} {sx} {sy} {sz} {{}}')
```

---

### 📘 Tutorial 7 – Random Mobs in a Circle

Summon random mobs in a circle around the player using a preset list.

```python
from time import sleep
import math
import random
from minescript import player_position, echo, execute

x, y, z = map(int, player_position())

mobs = ["allay", "bee", "parrot"]
num_mobs = 12
radius = 1

for i in range(num_mobs):
    angle = 2 * math.pi * i / num_mobs
    dx = round(math.cos(angle) * radius, 2)
    dz = round(math.sin(angle) * radius, 2)
    sx = x + dx
    sy = y
    sz = z + dz
    mob = random.choice(mobs)
    execute(f'/summon minecraft:{mob} {sx} {sy} {sz} {{}}')
```

