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


def get_pos_text(entity):
    """位置をきれいにフォーマット"""
    if not entity or not getattr(entity, "position", None):
        return "§7(??)§r"

    xyz = get_xyz(entity.position)
    if not xyz:
        return "§7(??)§r"

    x, y, z = xyz
    return f"§7({round(x,1)}, {round(y,1)}, {round(z,1)})§r"


COLOR = {
    "Player": "§9",
    "Mob": "§c",
    "Entity": "§d",
    "Source": "§e",
    "Reset": "§r"
}


while True:
    event = eq.get()
    if not event or event.type != EventType.DAMAGE:
        continue

    entity = resolve_entity(event.entity_uuid)
    cause = resolve_entity(event.cause_uuid)

    entity_name, entity_type = format_name(entity)
    cause_name, cause_type = format_name(cause)

    dist = distance(
        getattr(entity, "position", None),
        getattr(cause, "position", None)
    )

    source_text = f"{COLOR['Source']}{event.source}{COLOR['Reset']}"
    pos_text = get_pos_text(entity)

    msg = (
        f"💥 {COLOR.get(entity_type,'')}{entity_name}{COLOR['Reset']} "
        f"@ {pos_text} "
        f"-> {COLOR.get(cause_type,'')}{cause_name}{COLOR['Reset']} "
        f"[{source_text}]"
    )

    if dist is not None:
        msg += f" 📏{round(dist,1)}m"

    if entity and getattr(entity, "health", None) is not None:
        msg += f" ❤️{round(entity.health,1)}HP"

    m.echo(msg)
