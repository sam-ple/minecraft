import minescript as m
from minescript import EventQueue, EventType

eq = EventQueue()
eq.register_damage_listener()

m.echo("⚡ DamageEvent debug mode: waiting for damage...")

# --- UUID から名前を解決する関数 ---
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
        # カスタムネームがあればそれを使用
        if ent.nbt and "CustomName" in ent.nbt:
            name = ent.nbt["CustomName"]
        else:
            # entity.minecraft.zombie -> Zombie
            name = ent.type.split(":")[-1].replace("_", " ").title()
        return name, "Mob"
    
    return "Unknown", "?"

# --- Minecraftチャット用カラーコード ---
COLOR = {
    "Player": "§9",  # 青
    "Mob": "§c",     # 赤
    "Source": "§e",  # 黄色
    "Reset": "§r"    # リセット
}

while True:
    event = eq.get()
    if not event or event.type != EventType.DAMAGE:
        continue

    # エンティティ名と種類を解決
    entity_name, entity_type = resolve_name(event.entity_uuid)
    cause_name, cause_type = resolve_name(event.cause_uuid)

    # sourceを色付きで
    source_text = f"{COLOR['Source']}{event.source}{COLOR['Reset']}"

    # 出力文字列を作成
    output = f"💥 {COLOR.get(entity_type, '')}{entity_name}{COLOR['Reset']} -> {COLOR.get(cause_type, '')}{cause_name}{COLOR['Reset']} [{source_text}]"

    m.echo(output)
