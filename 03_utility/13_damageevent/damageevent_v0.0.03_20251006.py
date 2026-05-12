import minescript as m
from minescript import EventQueue, EventType

eq = EventQueue()
eq.register_damage_listener()

m.echo("⚡ DamageEvent debug mode: waiting for damage...")

def resolve_name(uuid):
    if not uuid:
        return "Unknown", "?"
    # プレイヤーかチェック
    players_list = m.players(uuid=uuid)
    if players_list:
        return players_list[0].name, "Player"
    # モブかチェック
    entities_list = m.entities(uuid=uuid)
    if entities_list:
        ent = entities_list[0]
        # カスタム名があれば使用
        if ent.nbt and "CustomName" in ent.nbt:
            name = ent.nbt["CustomName"]
        else:
            # entity.minecraft.zombie -> Zombie のように変換
            name = ent.type.split(":")[-1].capitalize()
        return name, "Mob"
    return "Unknown", "?"

# 色マップ
color_map = {
    "Player": "blue",
    "Mob": "red",
    "method": "yellow"
}

while True:
    event = eq.get()
    if not event or event.type != EventType.DAMAGE:
        continue

    # --- 名前解決 ---
    attacker_name, attacker_type = resolve_name(event.cause_uuid)
    victim_name, victim_type     = resolve_name(event.entity_uuid)
    method = event.source.replace("_", " ").capitalize()

    # tellraw 形式で出力（色付き）
    tellraw_json = [
        {"text": attacker_name, "color": color_map.get(attacker_type, "white")},
        {"text": " -> ", "color": "white"},
        {"text": victim_name, "color": color_map.get(victim_type, "white")},
        {"text": f" [{method}]", "color": color_map["method"]}
    ]

    m.execute(f'tellraw @a {tellraw_json}')
