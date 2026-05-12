import minescript as m
import time

ALLOWED_BLOCKS = [
    "minecraft:blue_concrete",  # 許可ブロック
]

m.echo("⚠️ 指定ブロック以外を踏むと死亡")

while True:
    for block_type in ALLOWED_BLOCKS:
        # 全プレイヤーをチェック
        m.execute(
            f"execute as @a at @s unless block ~ ~-1 ~ {block_type} run kill @s"
        )

    time.sleep(0.1)
