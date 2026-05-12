import minescript as m
from minescript import EventQueue, EventType
import time, math, json, threading, random

PLAYER = m.player_name()
BOSSBAR_ID = "minecraft:direction_bar"

# --- Constants ---
MAX_AMMO = 8
ammo = MAX_AMMO
FIRE_INTERVAL = 0.5

# --- Bossbar initialization ---
m.execute("gamerule sendCommandFeedback false")
m.execute("title @a clear")
m.execute(f"bossbar add {BOSSBAR_ID} Direction")
m.execute(f"bossbar set {BOSSBAR_ID} max 1")
m.execute(f"bossbar set {BOSSBAR_ID} value 1")
m.execute(f"bossbar set {BOSSBAR_ID} color white")
m.execute(f"bossbar set {BOSSBAR_ID} players {PLAYER}")

# --- Direction handling ---
degree_marks = [0,15,30,45,60,75,90,105,120,135,150,165,
                180,195,210,225,240,255,270,285,300,315,330,345]
direction_labels = {0:"S",90:"W",180:"N",270:"E"}

def build_bossbar_line(yaw):
    yaw = (yaw + 360) % 360
    idx = min(range(len(degree_marks)), key=lambda i: abs(degree_marks[i] - yaw))
    total = len(degree_marks)
    indices = [(idx + i) % total for i in range(-2, 3)]
    parts = []
    for i in indices:
        deg = degree_marks[i]
        label = direction_labels.get(deg, str(deg))
        if i == idx:
            parts.append(f"▶ {label} ◀")
        else:
            parts.append(f" {label} ")
    return "|".join(parts)

def update_bossbar_loop():
    last_line = None
    while True:
        yaw, pitch = m.player_orientation()
        line = build_bossbar_line(yaw)
        if line != last_line:
            name_json = json.dumps({"text": line, "color": "white"})
            m.execute(f"bossbar set {BOSSBAR_ID} name {name_json}")
            last_line = line
        time.sleep(0.1)

# --- Ammo handling ---
def update_ammo_display():
    filled = "■" * ammo
    empty = "□" * (MAX_AMMO - ammo)
    m.execute(f'title {PLAYER} actionbar {json.dumps({"text": filled+empty, "color":"gold"})}')

def ammo_display_loop():
    while True:
        update_ammo_display()
        time.sleep(0.2)

def reload_ammo():
    global ammo
    ammo = MAX_AMMO
    m.execute(f"clear {PLAYER} minecraft:iron_ingot 1")
    m.echo("🔄 Reloaded!")
    update_ammo_display()

# --- Weapon check ---
def spyglass_in_mainhand():
    hands = m.player_hand_items()
    if not hands or not hands.main_hand:
        return False
    if isinstance(hands.main_hand, dict):
        item = hands.main_hand.get("item", None)
    else:
        item = str(hands.main_hand)
    return item == "minecraft:spyglass"

def iron_ingot_in_mainhand():
    hands = m.player_hand_items()
    if not hands or not hands.main_hand:
        return False
    if isinstance(hands.main_hand, dict):
        item = hands.main_hand.get("item", None)
    else:
        item = str(hands.main_hand)
    return item == "minecraft:iron_ingot"

# --- Player eye position ---
def eye_pos():
    x, y, z = m.player_position()
    yaw, pitch = m.player_orientation()
    y += 1.62
    return x, y, z, yaw, pitch

# --- Fire projectile (snowball/arrow type) ---
def fire():
    global ammo
    if ammo <= 0:
        m.echo("❌ No ammo! Reload with iron ingot + Shift.")
        return
    ammo -= 1
    update_ammo_display()

    ex, ey, ez, yaw, pitch = eye_pos()
    rad_yaw = math.radians(yaw)
    rad_pitch = math.radians(pitch)

    # Motion vector
    dx = -math.sin(rad_yaw) * math.cos(rad_pitch) + random.uniform(-0.02,0.02)
    dy = -math.sin(rad_pitch) + random.uniform(-0.02,0.02)
    dz = math.cos(rad_yaw) * math.cos(rad_pitch) + random.uniform(-0.02,0.02)

    # Summon snowball
    m.execute(f"summon minecraft:snowball {ex} {ey} {ez} {{Motion:[{dx:.3f},{dy:.3f},{dz:.3f}]}}")
    m.execute(f"playsound minecraft:entity.arrow.shoot master {PLAYER}")

# --- Damage handler ---
def damage_loop():
    with EventQueue() as eq:
        eq.register_damage_listener()
        while True:
            e = eq.get()
            if e.type == EventType.DAMAGE:
                target = getattr(e,"target",None)
                source = getattr(e,"source",None)
                if target and source and source.get("type")=="snowball":
                    m.echo(f"💥 Hit {target.get('type','Unknown')} for {getattr(e,'amount',0)} damage!")

# --- Main ---
def main():
    global ammo
    m.echo("🎯 Sniper (Spyglass): Left click to shoot (snowball) / Direction shown in bossbar")
    m.echo("🔫 Ammo starts with 8 | Reload: hold iron ingot + Left Shift")

    # Start loops
    threading.Thread(target=update_bossbar_loop, daemon=True).start()
    threading.Thread(target=ammo_display_loop, daemon=True).start()
    threading.Thread(target=damage_loop, daemon=True).start()

    with EventQueue() as eq:
        eq.register_mouse_listener()
        eq.register_key_listener()
        last_shot = 0.0

        while True:
            e = eq.get()
            now = time.time()

            # Left click fire
            if e.type == EventType.MOUSE and e.button == 0 and e.action == 1:
                if not spyglass_in_mainhand():
                    continue
                if now - last_shot < FIRE_INTERVAL:
                    continue
                last_shot = now
                fire()

            # Reload: iron ingot + Left Shift release
            if e.type == EventType.KEY and e.action == 0:  # release
                if e.key == 340:
                    if iron_ingot_in_mainhand():
                        reload_ammo()

main()
