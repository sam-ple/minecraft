import minescript as m
from minescript import EventQueue, EventType
import math

eq = EventQueue()
eq.register_damage_listener()

m.echo("⚡ DamageEvent debug mode: waiting for damage...")

def resolve_entity(uuid):
    """UUIDからEntityDataを返す（Player優先）"""
    if not uuid:
        return None
    
    players_list = m.players(uuid=uuid)
    if players_list:
        return players_list[0]
    
    entities_list = m.entities(uuid=uuid)
    if entities_list:
        return entities_list[0]
    
    return None


def format_name(ent):
    """名前＋種別"""
    if ent is None:
        return "Unknown", "?"
    
    if getattr(ent, "local", False):
        return ent.name, "Player"
    elif "minecraft:" in getattr(ent, "type", ""):
        return ent.type.split(":")[-1].replace("_", " ").title(), "Mob"
    else:
        return getattr(ent, "name", None) or getattr(ent, "type", "?"), "Entity"


def get_xyz(pos):
    """posがlist/tupleまたはオブジェクトのどちらでも(x, y, z)を返す"""
    if pos is None:
        return None
    if isinstance(pos, (list, tuple)) and len(pos) >= 3:
        return pos[0], pos[1], pos[2]
    if all(hasattr(pos, k) for k in ("x", "y", "z")):
        return pos.x, pos.y, pos.z
    return None


def distance(pos1, pos2):
    """距離を計算"""
    a = get_xyz(pos1)
    b = get_xyz(pos2)
    if not a or not b:
        return None
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)


COLOR = {
    "Player": "§9",
    "Mob": "§c",
    "Entity": "§d",
    "Source": "§e",
    "Reset": "§r"
}

# 自然ダメージ系のソース一覧
ENVIRONMENTAL_SOURCES = {
    "fall", "drown", "lava", "fire", "cactus", "lightning", "starve",
    "suffocate", "explosion", "cramming", "freeze", "sweet_berry_bush", "magic"
}


while True:
    event = eq.get()
    if not event or event.type != EventType.DAMAGE:
        continue

    victim = resolve_entity(event.entity_uuid)
    attacker = resolve_entity(event.cause_uuid)

    victim_name, victim_type = format_name(victim)
    attacker_name, attacker_type = format_name(attacker)

    dist = distance(
        getattr(victim, "position", None),
        getattr(attacker, "position", None)
    )

    source = event.source.lower() if event.source else "unknown"
    source_text = f"{COLOR['Source']}{source}{COLOR['Reset']}"

    # 出力文（自然ダメージは矢印なし）
    if source in ENVIRONMENTAL_SOURCES or attacker_name == "Unknown":
        msg = f"💥 {COLOR.get(victim_type,'')}{victim_name}{COLOR['Reset']} took {source_text} damage"
    else:
        msg = (
            f"💥 {COLOR.get(attacker_type,'')}{attacker_name}{COLOR['Reset']} "
            f"---> {COLOR.get(victim_type,'')}{victim_name}{COLOR['Reset']} "
            f"[{source_text}]"
        )

    if dist is not None and source not in ENVIRONMENTAL_SOURCES:
        msg += f" 📏{round(dist,1)}m"

    if victim and getattr(victim, "health", None) is not None:
        msg += f" ❤️{round(victim.health,1)}HP"

    m.echo(msg)
