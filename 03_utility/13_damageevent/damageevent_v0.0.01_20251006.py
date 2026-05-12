import minescript as m
from minescript import EventQueue, EventType

eq = EventQueue()
eq.register_damage_listener()

m.echo("⚡ DamageEvent debug mode: waiting for damage...")

while True:
    event = eq.get()
    if not event or event.type != EventType.DAMAGE:
        continue

    # --- UUID からエンティティ名またはタイプを取得 ---
    def resolve_name(uuid):
        # プレイヤーか確認
        players_list = m.players(uuid=uuid)
        if players_list:
            return players_list[0].name
        # モブなど他のエンティティ
        entities_list = m.entities(uuid=uuid)
        if entities_list:
            ent = entities_list[0]
            # カスタム名があればそれを、なければタイプ
            if ent.nbt and "CustomName" in ent.nbt:
                return ent.nbt["CustomName"]
            return ent.type  # 例: minecraft:skeleton
        return "Unknown Entity"

    entity_name = resolve_name(event.entity_uuid)
    cause_name = resolve_name(event.cause_uuid) if event.cause_uuid else None

    # --- 情報を出力 ---
    m.echo(f"--- DAMAGE EVENT ---")
    m.echo(f"entity_uuid = {event.entity_uuid} -> {entity_name}")
    m.echo(f"cause_uuid  = {event.cause_uuid} -> {cause_name}")
    m.echo(f"source      = {event.source}")
    m.echo(f"full event  = {event.__dict__}")
