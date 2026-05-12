import minescript as m
import time
from minescript import EventQueue, EventType

# -------------------------
# 初期化
# -------------------------
eq = EventQueue()
eq.register_damage_listener()

dead_players = set()

m.echo("Complete Death Monitoring System Started")

# -------------------------
# ユーティリティ
# -------------------------
def resolve_entity(uuid):
    if not uuid:
        return None
    p = m.players(uuid=uuid)
    if p:
        return p[0]
    e = m.entities(uuid=uuid)
    if e:
        return e[0]
    return None

def handle_death(player):
    """死亡処理"""
    if player.uuid in dead_players:
        return
    dead_players.add(player.uuid)
    x, y, z = map(int, player.position)
    m.execute(f"setblock {x} {y} {z} minecraft:gold_block")
    m.execute(f'tellraw @a {{"text":"[DeathDebug] {player.name} died at {x},{y},{z}","color":"red"}}')
    m.echo(f"{player.name} died → gold block placed at {x},{y},{z}")

# -------------------------
# メインループ
# -------------------------
while True:

    # ---------- DAMAGEイベント監視 ----------
    event = eq.get()
    if event and event.type == EventType.DAMAGE:
        victim = resolve_entity(event.entity_uuid)
        if victim and victim.type == "minecraft:player" and victim.health is not None:
            if victim.health <= 0:
                handle_death(victim)

    # ---------- 全プレイヤー定期チェック ----------
    for p in m.players():
        if p.health is not None and p.health <= 0:
            handle_death(p)

    time.sleep(0.1)
