import minescript as m
import time

# ==================================================
# 狼のバリエーションリスト
# ==================================================
WOLF_VARIANTS = [
    "pale",
    "woods",
    "ashen",
    "black",
    "chestnut",
    "rusty",
    "spotted",
    "striped",
    "snowy"
]

# ==================================================
# 狼を順番に召喚する関数
# ==================================================
def summon_all_wolves():
    m.echo("🐺 Summoning all wolf variants...")
    x, y, z = m.player_position()
    for variant in WOLF_VARIANTS:
        nbt = (
            f'{{Health:8.0f,Sitting:0b,CollarColor:14b,variant:"minecraft:{variant}",'
            f'sound_variant:"minecraft:{variant}"}}'
        )
        m.execute(f'summon wolf {x} {y} {z} {nbt}')
        m.echo(f"🐺 Summoned wolf: {variant}")
        time.sleep(0.5)  # 少し間隔を空けると安定
    m.echo("✅ All wolves summoned!")

# ==================================================
# 実行
# ==================================================
summon_all_wolves()
