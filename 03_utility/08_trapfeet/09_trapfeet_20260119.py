import minescript as m
import time

m.echo("💣 足元TNT + 被ダメージで点火")

INTERVAL = 0.1 

# datapack の no_replace 相当
NO_REPLACE = {
    "minecraft:air",
    "minecraft:cave_air",
    "minecraft:void_air",
    "minecraft:water",
    "minecraft:lava",
    "minecraft:bedrock",
    "minecraft:obsidian",
    "minecraft:crying_obsidian",
    "minecraft:end_portal_frame",
    "minecraft:end_portal",
    "minecraft:end_gateway",
    "minecraft:barrier",
    "minecraft:structure_block",
    "minecraft:command_block",
    "minecraft:chain_command_block",
    "minecraft:repeating_command_block",
    "minecraft:jigsaw",
    "minecraft:structure_void",
    "minecraft:tnt",
}

# プレイヤーごとの前回HP
last_health = {}

# unless条件を組み立て
UNLESS_FLOOR = " ".join(
    f"unless block ~ ~-1 ~ {block}" for block in NO_REPLACE
)

while True:
    players = m.players()

    for p in players:
        selector = f"@a[uuid={p.uuid}]"

        # 初回登録（HP基準点）
        if p.uuid not in last_health:
            last_health[p.uuid] = p.health
            continue

        # -------------------------
        # 常時：足元をTNTブロックに
        # -------------------------
        m.execute(
            f"execute at {selector} "
            f"{UNLESS_FLOOR} "
            "run setblock ~ ~-1 ~ minecraft:tnt"
        )

        # -------------------------
        # 被ダメージ検知 → 点火
        # -------------------------
        if p.health < last_health[p.uuid]:
            m.execute(
                f"execute at {selector} "
                "run summon minecraft:tnt ~ ~-1 ~"
            )

        # HP更新
        last_health[p.uuid] = p.health

    time.sleep(INTERVAL)
