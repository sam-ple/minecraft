import minescript as m
import time
import math

FALL_INTERVAL = 5    # TNTを降らせる間隔（秒）
SPAWN_HEIGHT = 20    # プレイヤーの上空何ブロックからTNTを召喚するか
POST_LAND_DELAY = 10 # 着地後のティック数（0.5秒）

m.echo("💣 自動Fuse計算TNT降下（着地後0.5秒爆発）開始")

while True:
    # 自由落下時間をティック数で計算
    # Minecraft物理: 加速度0.04ブロック/tick²
    fall_ticks = math.sqrt(2 * SPAWN_HEIGHT / 0.04)
    
    # 着地後のFuseを追加
    fuse_ticks = max(1, int(fall_ticks + POST_LAND_DELAY))

    # プレイヤーの真上SPAWN_HEIGHTブロックにTNT召喚
    m.execute(
        f"execute as @a at @s run summon tnt ~ ~{SPAWN_HEIGHT} ~ {{Fuse:{fuse_ticks}}}"
    )

    time.sleep(FALL_INTERVAL)
