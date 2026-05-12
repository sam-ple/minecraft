import minescript as m
from minescript import EventQueue, EventType, player, entities
import time, math, json, threading, random

# ==================================================
# Constants
# ==================================================
MAX_AMMO = 8
FIRE_INTERVAL = 0.5
EYE_HEIGHT = 1.62
KEY_SHIFT = 340
BOSSBAR_ID = "minecraft:direction_bar"

DEGREE_MARKS = list(range(0, 360, 15))
DIRECTION_LABELS = {0: "S", 90: "W", 180: "N", 270: "E"}

PLAYER = m.player_name()
LOCAL_UUID = player().uuid

# ==================================================
# Weapon State
# ==================================================
class WeaponState:
    def __init__(self):
        self.ammo = MAX_AMMO
        self.last_shot = 0.0

    def can_fire(self):
        return self.ammo > 0

    def consume_ammo(self):
        self.ammo -= 1

    def reload(self):
        self.ammo = MAX_AMMO
        m.execute(f"clear {PLAYER} minecraft:iron_ingot 1")
        m.echo("🔄 Reloaded!")

state = WeaponState()

# ==================================================
# Utility
# ==================================================
def eye_position():
    x, y, z = m.player_position()
    yaw, pitch = m.player_orientation()
    return x, y + EYE_HEIGHT, z, yaw, pitch

def holding(item_id: str) -> bool:
    hands = m.player_hand_items()
    if not hands or not hands.main_hand:
        return False
    item = hands.main_hand.get("item") if isinstance(hands.main_hand, dict) else str(hands.main_hand)
    return item == item_id

# ==================================================
# HUD (Bossbar & Ammo)
# ==================================================
def yaw_to_index(yaw):
    yaw = (yaw + 360) % 360
    return min(range(len(DEGREE_MARKS)), key=lambda i: abs(DEGREE_MARKS[i] - yaw))

def build_compass(yaw, span=2):
    idx = yaw_to_index(yaw)
    total = len(DEGREE_MARKS)
    parts = []

    for offset in range(-span, span + 1):
        i = (idx + offset) % total
        deg = DEGREE_MARKS[i]
        label = DIRECTION_LABELS.get(deg, str(deg))
        parts.append(f"▶ {label} ◀" if i == idx else f" {label} ")

    return "|".join(parts)

def update_bossbar_loop():
    last = None
    while True:
        yaw, _ = m.player_orientation()
        line = build_compass(yaw)
        if line != last:
            m.execute(f"bossbar set {BOSSBAR_ID} name {json.dumps({'text': line})}")
            last = line
        time.sleep(0.1)

def update_ammo():
    filled = "■" * state.ammo
    empty = "□" * (MAX_AMMO - state.ammo)
    m.execute(
        f"title {PLAYER} actionbar "
        f"{json.dumps({'text': filled + empty, 'color': 'gold'})}"
    )

def ammo_loop():
    while True:
        update_ammo()
        time.sleep(0.2)

# ==================================================
# Weapon Actions
# ==================================================
def fire():
    if not state.can_fire():
        m.echo("❌ No ammo! Reload with iron ingot + Shift.")
        return

    state.consume_ammo()
    update_ammo()

    x, y, z, yaw, pitch = eye_position()
    ry, rp = math.radians(yaw), math.radians(pitch)

    dx = -math.sin(ry) * math.cos(rp) + random.uniform(-0.02, 0.02)
    dy = -math.sin(rp) + random.uniform(-0.02, 0.02)
    dz =  math.cos(ry) * math.cos(rp) + random.uniform(-0.02, 0.02)

    m.execute(
        f"summon minecraft:arrow {x} {y} {z} "
        f"{{Motion:[{dx:.3f},{dy:.3f},{dz:.3f}]}}"
    )
    m.execute(f"playsound minecraft:entity.arrow.shoot master {PLAYER}")

# ==================================================
# Damage Monitor
# ==================================================
def damage_monitor_loop():
    eq = EventQueue()
    eq.register_damage_listener()

    while True:
        e = eq.get()
        if not e or e.type != EventType.DAMAGE:
            continue
        if e.cause_uuid != LOCAL_UUID:
            continue

        mob = entities(uuid=e.entity_uuid)
        if not mob:
            continue

        mob = mob[0]
        hp = getattr(mob, "health", None)

        if hp is None:
            m.echo(f"🎯 Hit {mob.type}!")
        elif hp > 0:
            m.echo(f"🎯 Hit {mob.type}! (HP: {hp})")
        else:
            m.echo(f"💀 Killed {mob.type}!")

# ==================================================
# Main
# ==================================================
def init_bossbar():
    m.execute("gamerule sendCommandFeedback false")
    m.execute("title @a clear")
    m.execute(f"bossbar add {BOSSBAR_ID} Direction")
    m.execute(f"bossbar set {BOSSBAR_ID} max 1")
    m.execute(f"bossbar set {BOSSBAR_ID} value 1")
    m.execute(f"bossbar set {BOSSBAR_ID} players {PLAYER}")

def main():
    m.echo("🎯 Arrow Sniper v2 (Refactored)")
    m.echo("🔫 Spyglass: Fire | Iron Ingot + Shift: Reload")

    init_bossbar()

    threading.Thread(target=update_bossbar_loop, daemon=True).start()
    threading.Thread(target=ammo_loop, daemon=True).start()
    threading.Thread(target=damage_monitor_loop, daemon=True).start()

    with EventQueue() as eq:
        eq.register_mouse_listener()
        eq.register_key_listener()

        while True:
            e = eq.get()
            now = time.time()

            if e.type == EventType.MOUSE and e.button == 0 and e.action == 1:
                if holding("minecraft:spyglass") and now - state.last_shot >= FIRE_INTERVAL:
                    state.last_shot = now
                    fire()

            if e.type == EventType.KEY and e.key == KEY_SHIFT and e.action == 0:
                if holding("minecraft:iron_ingot"):
                    state.reload()

main()
