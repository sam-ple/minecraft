import minescript as m
from minescript import EventQueue, EventType

eq = EventQueue()
eq.register_damage_listener()

m.echo("⚡ DamageEvent debug mode: waiting for damage...")

def resolve_name(uuid):
    """UUID からプレイヤー名かモブのタイプを返す"""
    if not uuid:
        return "None"
    players_list = m.players(uuid=uuid)
    if players_list:
        return players_list[0].name  # プレイヤー名
    entities_list = m.entities(uuid=uuid)
    if entities_list:
        ent = entities_list[0]
        if ent.nbt and "CustomName" in ent.nbt:
            return ent.nbt["CustomName"]
        return ent.type.split(":")[-1].capitalize()  # minecraft:skeleton → Skeleton
    return "Unknown Entity"

while True:
    event = eq.get()
    if not event or event.type != EventType.DAMAGE:
        continue

    attacker = resolve_name(event.cause_uuid)
    victim   = resolve_name(event.entity_uuid)
    method   = event.source.replace("_", " ").capitalize()
    damage   = getattr(event, "amount", "?")  # amount があれば表示

    # チャット表示
    m.echo(f"💥 {attacker} -> {victim} ({method} / {damage} dmg)")
