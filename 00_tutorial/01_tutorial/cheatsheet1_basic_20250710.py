import minescript as m
import time

# Currently Creating: Minescript Cheatsheet #1 – Learn the Basics

def title_subtitle(title_text, subtitle_text=None, title_color="gold", subtitle_color="aqua", delay=1):
    m.execute("title @a clear")
    m.execute(f'title @a title {{"text":"{title_text}","color":"{title_color}","bold":true}}')
    if subtitle_text and subtitle_text.strip():
        m.execute(f'title @a subtitle {{"text":"{subtitle_text}","color":"{subtitle_color}","bold":true}}')
    time.sleep(delay)

# --- Basic Commands and Chat ---

title_subtitle("execute", "Give emerald")
m.echo("--------------")
m.echo("01 Execute: Give emerald")
m.execute("give @s minecraft:emerald 1")
time.sleep(2)

title_subtitle("echo", "Private message")
m.echo("--------------")
m.echo("02 Echo: Private message")
m.echo("This is a private message")
time.sleep(2)

title_subtitle("echo_json", "Red colored text")
m.echo("--------------")
m.echo("03 Echo JSON: Red colored text")
m.echo_json({"text": "This is red text", "color": "red"})
time.sleep(2)

title_subtitle("chat", "Send public chat message")
m.echo("--------------")
m.echo("04 Chat: Send public chat message")
m.chat("Hello from Minescript!")
time.sleep(2)

title_subtitle("log", "Write to latest.log")
m.echo("--------------")
m.echo("05 Log: Write to latest.log")
m.log("This is a log entry from Minescript")
time.sleep(2)

title_subtitle("screenshot", "Take screenshot")
m.echo("--------------")
m.echo("06 Screenshot: Take screenshot")
m.screenshot("sample_screenshot")
time.sleep(2)

# --- Job & Command Control ---

title_subtitle("job_info", "List current jobs")
m.echo("--------------")
m.echo("07 Job Info: List current jobs")
for job in m.job_info():
    m.echo(f"Job ID: {job.job_id}, Status: {job.status}, Self: {job.self}")
time.sleep(2)

title_subtitle("flush", "Wait for all commands to complete")
m.echo("--------------")
m.echo("08 Flush: Wait for all commands to complete")
m.flush()
time.sleep(2)

# --- Player Information ---

title_subtitle("player_name", "Get current player's name")
name = m.player_name()
m.echo("--------------")
m.echo(f"09 Player Name: {name}")
time.sleep(2)

title_subtitle("player_position", "Get current coordinates")
pos = m.player_position()
m.echo("--------------")
m.echo(f"10 Player Position: X={pos[0]:.2f}, Y={pos[1]:.2f}, Z={pos[2]:.2f}")
x, y, z = map(int, m.player_position())
m.echo(f"X={x}, Y={y}, Z={z}")
time.sleep(2)

title_subtitle("player_hand_items")
import random
weapons = ["diamond_sword", "netherite_sword", "iron_axe", "bow", "crossbow"]
helmets = ["diamond_helmet", "netherite_helmet", "iron_helmet", "golden_helmet", "leather_helmet"]
chestplates = ["diamond_chestplate", "netherite_chestplate", "iron_chestplate", "golden_chestplate", "leather_chestplate"]
leggings = ["diamond_leggings", "netherite_leggings", "iron_leggings", "golden_leggings", "leather_leggings"]
boots = ["diamond_boots", "netherite_boots", "iron_boots", "golden_boots", "leather_boots"]
shields = ["shield", "totem_of_undying", "bow", "torch", "ender_pearl"]
m.execute(f'item replace entity @p weapon.mainhand with minecraft:{random.choice(weapons)}')
m.execute(f'item replace entity @p armor.head with minecraft:{random.choice(helmets)}')
m.execute(f'item replace entity @p armor.chest with minecraft:{random.choice(chestplates)}')
m.execute(f'item replace entity @p armor.legs with minecraft:{random.choice(leggings)}')
m.execute(f'item replace entity @p armor.feet with minecraft:{random.choice(boots)}')
m.execute(f'item replace entity @p weapon.offhand with minecraft:{random.choice(shields)}')
time.sleep(0.5)
hands = m.player_hand_items()
m.echo("--------------")
m.echo(f"11 Player Hand Items:")
m.echo(f" - Main hand: {hands.main_hand.item} x{hands.main_hand.count}")
m.echo(f" - Off hand: {hands.off_hand.item} x{hands.off_hand.count}")
time.sleep(2)

title_subtitle("player_inventory", "Player Inventory (first 5 slots)")
items_to_set = [
    ("minecraft:emerald", 10),
    ("minecraft:diamond", 5),
    ("minecraft:apple", 20),
    ("minecraft:cooked_beef", 12),
    ("minecraft:bread", 7),
    ("minecraft:torch", 64),
    ("minecraft:iron_pickaxe", 1),
    ("minecraft:oak_log", 32),
    ("minecraft:arrow", 64),
    ("minecraft:golden_carrot", 8),
    ("minecraft:water_bucket", 1),
    ("minecraft:shield", 1),
]
for item_id, count in items_to_set:
    m.execute(f'give @p {item_id} {count}')
time.sleep(0.5)
inv = m.player_inventory()
m.echo("--------------")
m.echo("12 Player Inventory (first 5 slots):")
for item in inv[:5]:
    m.echo(f" Slot {item.slot}: {item.item} x{item.count}")
time.sleep(2)

title_subtitle("player_inventory_select_slot", "Switch hotbar slot to 1")
prev_slot = m.player_inventory_select_slot(1)
m.echo("--------------")
m.echo(f"13 Switch hotbar slot to 1 (previous slot: {prev_slot})")
time.sleep(2)

# --- Player Actions (Key Press Simulation) ---

title_subtitle("press_key_bind")
m.echo("--------------")
m.echo("14 Press multiple key binds sequentially")

actions = [
    ("key.jump", 0.2),
    ("key.hotbar.4", 0.2),
    ("key.sneak", 1.0),
    ("key.use", 0.5),
]

for key, duration in actions:
    m.echo(f"Pressing {key} for {duration} seconds")
    m.press_key_bind(key, True)   
    time.sleep(duration)          
    m.press_key_bind(key, False)  
    m.echo(f"Released {key}")
    time.sleep(0.5)               

time.sleep(2)

# Valid values of key_mapping_name include: “key.advancements”, “key.attack”, “key.back”, “key.chat”, “key.command”, “key.drop”, “key.forward”, “key.fullscreen”, “key.hotbar.1”, “key.hotbar.2”, “key.hotbar.3”, “key.hotbar.4”, “key.hotbar.5”, “key.hotbar.6”, “key.hotbar.7”, “key.hotbar.8”, “key.hotbar.9”, “key.inventory”, “key.jump”, “key.left”, “key.loadToolbarActivator”, “key.pickItem”, “key.playerlist”, “key.right”, “key.saveToolbarActivator”, “key.screenshot”, “key.smoothCamera”, “key.sneak”, “key.socialInteractions”, “key.spectatorOutlines”, “key.sprint”, “key.swapOffhand”, “key.togglePerspective”, “key.use”


title_subtitle("player_press_xxx")
m.echo("--------------")
m.echo("15 Player movement key presses")

# --- Forward ---
m.echo("moving forward")
m.player_press_forward(True)
time.sleep(1)
m.player_press_forward(False)
m.echo(" Stopped moving forward")

# --- Backward ---
m.echo("moving backward")
m.player_press_backward(True)
time.sleep(1)
m.player_press_backward(False)
m.echo(" Stopped moving backward")

# --- Left ---
m.echo("moving left")
m.player_press_left(True)
time.sleep(1)
m.player_press_left(False)
m.echo(" Stopped moving left")

# --- Right ---
m.echo("moving right")
m.player_press_right(True)
time.sleep(1)
m.player_press_right(False)
m.echo(" Stopped moving right")

# --- Jump x2 ---
m.echo("jump")
m.player_press_jump(True)
time.sleep(0.3)
m.player_press_jump(False)
time.sleep(0.2)
m.player_press_jump(True)
time.sleep(0.3)
m.player_press_jump(False)
time.sleep(0.2)

# --- Sprint ---
m.echo("sprint")
m.player_press_sprint(True)
time.sleep(1)
m.player_press_sprint(False)
m.echo(" Stopped sprinting")

# --- Sneak ---
m.echo("sneak")
m.player_press_sneak(True)
time.sleep(1)
m.player_press_sneak(False)
m.echo(" Stopped sneaking")

# --- Pick Item ---
m.echo("pick item")
m.player_press_pick_item(True)
time.sleep(0.2)
m.player_press_pick_item(False)

# --- Use Item ---
m.echo("use item")
m.player_press_use(True)
time.sleep(0.5)
m.player_press_use(False)

# --- Attack ---
m.echo("attack")
m.player_press_attack(True)
time.sleep(0.5)
m.player_press_attack(False)

# --- Swap Hands ---
m.echo("swap_hands")
m.player_press_swap_hands(True)
time.sleep(0.2)
m.player_press_swap_hands(False)

# --- Drop ---
m.echo("drop")
m.player_press_drop(True)
time.sleep(0.2)
m.player_press_drop(False)

time.sleep(2)

# --- View & Orientation ---

title_subtitle("player_orientation")
m.echo("--------------")
yaw, pitch = m.player_orientation()
m.echo(f"16 Player Orientation: Yaw={yaw:.1f}, Pitch={pitch:.1f}")
time.sleep(2)

title_subtitle("set_orientation")
m.echo("--------------")
m.echo("17 Set orientation: Turn 180 degrees and level pitch")
success = m.player_set_orientation(yaw + 180, 0)
m.echo("Orientation changed" if success else "Failed to set orientation")
time.sleep(2)

# --- Targeting ---

title_subtitle("player_get_targeted_block","Get targeted block (within 20 blocks)")
x, y, z = m.player_position()
yaw, pitch = m.player_orientation()
import math
rad = math.radians(yaw)
dx = round(-math.sin(rad))
dz = round(math.cos(rad))
bx = int(x + dx * 2)
by = int(y)
bz = int(z + dz * 2)
m.execute(f'setblock {bx} {by} {bz} minecraft:diamond_block')
time.sleep(0.5)
m.echo("--------------")
m.echo("18 Get targeted block (within 20 blocks)")
tblock = m.player_get_targeted_block(20)
if tblock:
    m.echo(f"Target Block: {tblock.type} at {tblock.position}, side: {tblock.side}")
else:
    m.echo("No block targeted")
time.sleep(2)

title_subtitle("player_get_targeted_entity","Get targeted entity (within 20 blocks)")
x, y, z = m.player_position()
yaw, pitch = m.player_orientation()
import math
rad = math.radians(yaw)
dx = round(-math.sin(rad))
dz = round(math.cos(rad))
bx = int(x + dx * 2)
by = int(y)
bz = int(z + dz * 2)
m.execute(f'summon cow {bx} {by} {bz} {{NoGravity:1b,Invisible:0b}}')
time.sleep(0.5)
m.echo("--------------")
m.echo("19 Get targeted entity (within 20 blocks)")
target_entity = m.player_get_targeted_entity(20)
if target_entity:
    health = target_entity.health if target_entity.health is not None else "N/A"
    m.echo(f"Target Entity: {target_entity.name}, Type: {target_entity.type}, Health: {health}")
else:
    m.echo("No entity targeted")
time.sleep(2)

# --- Player Status ---

title_subtitle("player_health")
hp = m.player_health()
m.echo("--------------")
m.echo(f"20 Player Health: {hp}")
time.sleep(2)

title_subtitle("player")
pdata = m.player()
m.echo("--------------")
m.echo(f"21 Player Info: {pdata.name}, UUID={pdata.uuid}, HP={pdata.health}, Pos={pdata.position}")
time.sleep(2)

# --- Nearby Players and Entities ---

title_subtitle("players","Nearby players (max 5, nearest first)")
pos = m.player_position()
m.echo("--------------")
m.echo("22 Nearby players (max 5, nearest first)")
players = m.players(limit=5, sort="nearest")
for p in players:
    dist = ((p.position[0]-pos[0])**2 + (p.position[1]-pos[1])**2 + (p.position[2]-pos[2])**2)**0.5
    m.echo(f"Player: {p.name}, Distance ≈ {dist:.1f}")
time.sleep(2)

title_subtitle("entities","Nearby entities (max 5, nearest first)")
m.echo("--------------")
m.echo("23 Nearby entities (max 5, nearest first)")
entities = m.entities(limit=5, sort="nearest")
for e in entities:
    m.echo(f"Entity: {e.type}, Position={e.position}, HP={e.health}")
time.sleep(2)

# --- Version and World Information ---

title_subtitle("version_info")
m.echo("--------------")
ver = m.version_info()
m.echo(f"24 Version Info: Minecraft {ver.minecraft}, Minescript {ver.minescript}")
m.echo(f"ModLoader: {ver.mod_loader}, OS: {ver.os_name} {ver.os_version}")
time.sleep(1)

title_subtitle("world_info")
m.echo("--------------")
world = m.world_info()
m.echo(f"25 World Info: {world.name}, Seed Address: {world.address}")
m.echo(f"Time: {world.day_ticks} ticks, Weather: {'Rain' if world.raining else 'Clear'}, Difficulty: {world.difficulty}")
time.sleep(1)

# --- Block Queries ---

title_subtitle("getblock","Block under player feet")
pos = m.player_position()
feet_block = m.getblock(int(pos[0]), int(pos[1]) - 1, int(pos[2]))
m.echo("--------------")
m.echo(f"26 Block under player feet: {feet_block}")
time.sleep(2)

title_subtitle("getblocklist", "Multiple blocks near player")
pos = m.player_position()
positions = [
    [int(pos[0]), int(pos[1]) - 1, int(pos[2])],
    [int(pos[0]) + 1, int(pos[1]) - 1, int(pos[2])],
    [int(pos[0]), int(pos[1]) - 1, int(pos[2]) + 1],
]
blocks = m.getblocklist(positions)
m.echo("--------------")
m.echo("27 Multiple blocks near player:")
for p, b in zip(positions, blocks):
    m.echo(f" Block at {p}: {b}")
time.sleep(2)

title_subtitle("await_loaded_region","Await chunk loading around player")
m.echo("--------------")
m.echo("28 Await chunk loading around player (±128 blocks)")
m.await_loaded_region(int(pos[0]) - 128, int(pos[2]) - 128, int(pos[0]) + 128, int(pos[2]) + 128)
m.echo("Chunks loaded.")
time.sleep(2)

# --- GUI & Chat Interaction ---

title_subtitle("screen_name","Checking current screen name")
m.echo("--------------")
m.echo("29 Checking current screen name...")
screen = m.screen_name()
if screen:
    m.echo(f"Current screen: {screen}")
else:
    m.echo("No GUI screen is currently open.")
time.sleep(2)

title_subtitle("show_chat_screen","Opening chat screen with prompt")
m.echo("--------------")
m.echo("30 Opening chat screen with prompt '!hello'...")
success = m.show_chat_screen(True, prompt="!hello")
m.echo(f"Chat screen shown: {success}")
time.sleep(3) 
m.show_chat_screen(False)
time.sleep(2)

title_subtitle("chat_input","Getting current chat input text and cursor position")
m.echo("--------------")
m.echo("31 Getting current chat input text and cursor position...")
text, cursor = m.chat_input()
m.echo(f"Chat input: '{text}' (cursor at position {cursor})")
time.sleep(2)

title_subtitle("set_chat_input","Setting chat input to 'Updated text!' in red")
m.echo("--------------")
m.echo("32 Setting chat input to 'Updated text!' in red...")
m.set_chat_input(text="Updated text!", position=len("Updated text!"), color=0xFF0000)
time.sleep(2)
text, cursor = m.chat_input()
m.echo(f"Now input: '{text}' (cursor at {cursor})")
time.sleep(2)

title_subtitle("append_chat_history","Adding to chat history")
m.echo("--------------")
m.echo("33 Adding to chat history: '/warp test'")
m.append_chat_history("/warp test")
m.echo("Now try pressing ↑ in chat input to see it.")
m.show_chat_screen(True)
time.sleep(2)

# --- Container Inventory ---

title_subtitle("container_get_items","Check open container items")
m.echo("--------------")
m.echo("34 Check open container items")

items = m.container_get_items()
if items:
    for item in items:
        m.echo(f"- {item.count}x {item.item}")
else:
    m.echo("No open container or no items found.")
time.sleep(2)

# --- View Control: Camera Look At ---

title_subtitle("player_look_at","Rotate camera to a block 5 blocks ahead")
pos = m.player_position()
m.echo("--------------")
m.echo("35 Rotate camera to a block 5 blocks ahead")
x, y, z = pos[0] + 5, pos[1], pos[2]
m.player_look_at(x, y, z)
m.echo(f"Looking at position: ({x}, {y}, {z})")
time.sleep(2)

m.echo("Minescript Basic Test Complete!")
