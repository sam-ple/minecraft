import minescript as m
from minescript import EventQueue, EventType

with EventQueue() as eq:
    eq.register_damage_listener()

    m.echo("⚡ Swap Position on Hit")

    while True:
        event = eq.get()

        if event.type != EventType.DAMAGE:
            continue

        # プレイヤー取得
        victim_list = m.players(uuid=event.entity_uuid)
        attacker_list = m.players(uuid=event.cause_uuid) if event.cause_uuid else []

        # PvPのみ
        if not victim_list or not attacker_list:
            continue

        victim = victim_list[0]
        attacker = attacker_list[0]

        # 自分自身ダメージは除外（念のため）
        if victim.uuid == attacker.uuid:
            continue

        # 座標取得
        vx, vy, vz = victim.position
        ax, ay, az = attacker.position

        # 入れ替え
        m.execute(f"tp {victim.name} {ax} {ay} {az}")
        m.execute(f"tp {attacker.name} {vx} {vy} {vz}")

        m.echo(f"💥 SWAP {attacker.name} ↔ {victim.name}")
