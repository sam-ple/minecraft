import minescript as m
from minescript import EventQueue, EventType, player, entities
import time, math, json, threading, random

PLAYER = m.player_name()
local_uuid = player().uuid
BOSSBAR_ID = "minecraft:direction_bar"

# --- Constants ---
MAX_AMMO = 8
ammo = MAX_AMMO
FIRE_INTERVAL = 0.5  # seconds between shots

# --- Bossbar initialization ---
m.execute("gamerule sendCommandFeedback false")
m.execute("title @a clear")
m.execute(f"bossbar add {BOSSBAR_ID} Direction")
m.execute(f"bossbar set {BOSSBAR_ID} max 1")
m.execute(f"bossbar set {BOSSBAR_ID} value 1")
m.execute(f"bossbar set {BOSSBAR_ID} color white")
m.execute(f"bossbar set {BOSSBAR_ID} players {PLAYER}")

# --- Compass-like bossbar display ---
degree_marks = [i for i in range(0, 360, 15)]
direction_labels = {0: "S", 90: "W", 180: "N", 270: "E"}

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

# --- Weapon checks ---
def spyglass_in_mainhand():
    hands = m.player_hand_items()
    if not hands or not hands.main_hand:
        return False
    item = hands.main_hand.get("item") if isinstance(hands.main_hand, dict) else str(hands.main_hand)
    return item == "minecraft:spyglass"

def iron_ingot_in_mainhand():
    hands = m.player_hand_items()
    if not hands or not hands.main_hand:
        return False
    item = hands.main_hand.get("item") if isinstance(hands.main_hand, dict) else str(hands.main_hand)
    return item == "minecraft:iron_ingot"

# --- Player eye position ---
def eye_pos():
    x, y, z = m.player_position()
    yaw, pitch = m.player_orientation()
    y += 1.62  # eye height
    return x, y, z, yaw, pitch

# --- Fire custom arrow ---
def fire():
    global ammo
    if ammo <= 0:
        m.echo("❌ No ammo! Reload with iron ingot + Left Shift.")
        return
    ammo -= 1
    update_ammo_display()

    ex, ey, ez, yaw, pitch = eye_pos()
    rad_yaw = math.radians(yaw)
    rad_pitch = math.radians(pitch)

    dx = -math.sin(rad_yaw) * math.cos(rad_pitch) + random.uniform(-0.02, 0.02)
    dy = -math.sin(rad_pitch) + random.uniform(-0.02, 0.02)
    dz = math.cos(rad_yaw) * math.cos(rad_pitch) + random.uniform(-0.02, 0.02)

    # Summon arrow (tag not required for detection)
    m.execute(f'summon minecraft:arrow {ex} {ey} {ez} {{Motion:[{dx:.3f},{dy:.3f},{dz:.3f}]}}')
    m.execute(f"playsound minecraft:entity.arrow.shoot master {PLAYER}")

# --- Damage event monitoring ---
def damage_monitor_loop():
    eq = EventQueue()
    eq.register_damage_listener()
    while True:
        e = eq.get()
        if not e or e.type != EventType.DAMAGE:
            continue
        # Only our own damage events
        if e.cause_uuid != local_uuid:
            continue
        if e.source not in ["player", "arrow", "trident"]:
            continue

        mobs = entities(uuid=e.entity_uuid)
        if not mobs:
            continue

        mob = mobs[0]
        hp = getattr(mob, "health", None)
        if hp is not None:
            if hp > 0:
                m.echo(f"🎯 Hit {mob.type}! (HP left: {hp})")
            else:
                m.echo(f"💀 Killed {mob.type}!")
        else:
            m.echo(f"🎯 Hit {mob.type}!")

# --- Main ---
def main():
    m.echo("🎯 Arrow Sniper: Detects hits (HP & kill tracking)")
    m.echo("🔫 Ammo: 8 shots | Reload with iron ingot + Left Shift")

    threading.Thread(target=update_bossbar_loop, daemon=True).start()
    threading.Thread(target=ammo_display_loop, daemon=True).start()
    threading.Thread(target=damage_monitor_loop, daemon=True).start()

    with EventQueue() as eq:
        eq.register_mouse_listener()
        eq.register_key_listener()
        last_shot = 0.0

        while True:
            e = eq.get()
            now = time.time()

            # Left click to fire
            if e.type == EventType.MOUSE and e.button == 0 and e.action == 1:
                if not spyglass_in_mainhand():
                    continue
                if now - last_shot < FIRE_INTERVAL:
                    continue
                last_shot = now
                fire()

            # Release Left Shift + holding iron ingot → reload
            if e.type == EventType.KEY and e.action == 0 and e.key == 340:
                if iron_ingot_in_mainhand():
                    reload_ammo()

main()
