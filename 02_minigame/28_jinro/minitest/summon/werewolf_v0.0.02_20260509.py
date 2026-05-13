import minescript as m
import math
import random
import time
import sys

# =========================================================
# SETTINGS
# =========================================================
WORLD_BORDER_RADIUS = 200

NUM_SKELETONS = 200
NUM_WITHER = 100

TICK = 0.1

PLAYERS = ["crocadooo", "saaample"]

# =========================================================
# ARG
# =========================================================
arg = sys.argv[1] if len(sys.argv) >= 2 else ""

# =========================================================
# summon
# =========================================================
if arg == "summon":

    player = m.player()
    px, py, pz = player.position

    px = math.floor(px)
    pz = math.floor(pz)

    m.execute("time set night")
    m.execute("gamerule sendCommandFeedback false")
    m.execute("gamerule doMobLoot false")

    # ワールドボーダー
    m.execute(f"worldborder center {px} {pz}")
    m.execute(f"worldborder set {WORLD_BORDER_RADIUS * 2}")

    # =========================================
    # スケルトン
    # =========================================
    for _ in range(NUM_SKELETONS):

        m.execute(
            f"summon minecraft:skeleton {px} {py+5} {pz} "
            "{"
            "Tags:[\"spread_skeleton\"],"
            "NoAI:1b,"
            "PersistenceRequired:1b,"
            "Health:2f"
            "}"
        )

    # =========================================
    # ウィザースケルトン
    # =========================================
    for _ in range(NUM_WITHER):

        m.execute(
            f"summon minecraft:wither_skeleton {px} {py+5} {pz} "
            "{"
            "Tags:[\"spread_wither\"],"
            "NoAI:1b,"
            "PersistenceRequired:1b,"
            "Health:5f"
            "}"
        )

    # =========================================
    # 分散
    # =========================================
    m.execute(
        f"spreadplayers {px} {pz} 10 {WORLD_BORDER_RADIUS} false "
        "@e[tag=spread_skeleton]"
    )

    m.execute(
        f"spreadplayers {px} {pz} 10 {WORLD_BORDER_RADIUS} false "
        "@e[tag=spread_wither]"
    )

    m.echo(
        f"✅ Skeleton {NUM_SKELETONS} / "
        f"Wither {NUM_WITHER}"
    )

# =========================================================
# get
# =========================================================
elif arg == "get":

    # =========================================
    # objectives
    # =========================================
    m.execute(
        "scoreboard objectives add SkeletonKill "
        "minecraft.killed:minecraft.skeleton"
    )

    m.execute(
        "scoreboard objectives add WitherKill "
        "minecraft.killed:minecraft.wither_skeleton"
    )

    m.execute("scoreboard objectives add PrevSkeleton dummy")
    m.execute("scoreboard objectives add PrevWither dummy")

    m.execute("scoreboard objectives add DiffSkeleton dummy")
    m.execute("scoreboard objectives add DiffWither dummy")

    print("Reward Start")

    WITHER_ITEMS = [
        "minecraft:cooked_beef",
        "minecraft:trident",
        "minecraft:snowball",
        "minecraft:bow",
        "minecraft:arrow"
    ]

    while True:

        # =================================================
        # Skeleton Diff
        # =================================================
        m.execute(
            "execute as @a run "
            "scoreboard players operation "
            "@s DiffSkeleton = @s SkeletonKill"
        )

        m.execute(
            "execute as @a run "
            "scoreboard players operation "
            "@s DiffSkeleton -= @s PrevSkeleton"
        )

        # =================================================
        # Wither Diff
        # =================================================
        m.execute(
            "execute as @a run "
            "scoreboard players operation "
            "@s DiffWither = @s WitherKill"
        )

        m.execute(
            "execute as @a run "
            "scoreboard players operation "
            "@s DiffWither -= @s PrevWither"
        )

        time.sleep(0.02)

        # =================================================
        # プレイヤー取得
        # =================================================

        for name in PLAYERS:
    
            # =============================================
            # Skeleton reward
            # =============================================
            if random.randint(0, 1) == 1:

                m.execute(
                    f"execute as {name} "
                    "if score @s DiffSkeleton matches 1.. "
                    "run give @s minecraft:emerald 1"
                )

                m.execute(
                    f'execute as {name} '
                    'if score @s DiffSkeleton matches 1.. '
                    'run tellraw @s '
                    '{"text":"Lucky Emerald!","color":"green"}'
                )

            # =============================================
            # Wither reward
            # =============================================
            item = random.choice(WITHER_ITEMS)

            m.execute(
                f"execute as {name} "
                "if score @s DiffWither matches 1.. "
                f"run give @s {item} 1"
            )

            m.execute(
                f'execute as {name} '
                'if score @s DiffWither matches 1.. '
                'run tellraw @s '
                '{"text":"Wither Reward!","color":"gold"}'
            )

        # =================================================
        # Prev更新
        # =================================================
        m.execute(
            "execute as @a run "
            "scoreboard players operation "
            "@s PrevSkeleton = @s SkeletonKill"
        )

        m.execute(
            "execute as @a run "
            "scoreboard players operation "
            "@s PrevWither = @s WitherKill"
        )

        time.sleep(TICK)

# =========================================================
# help
# =========================================================
else:

    m.echo("Usage:")
