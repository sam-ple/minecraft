import minescript as m
import math
import time

player = m.player()
px, py, pz = player.position

px = math.floor(px)
py = math.floor(py)
pz = math.floor(pz)

R = 50
NUM = 10

# =========================
# 仮エンティティ召喚
# =========================
for _ in range(NUM):
    m.execute(
        f"summon armor_stand {px} {py+5} {pz} "
        "{Invisible:1b,Marker:1b,NoGravity:1b,Tags:[\"chestpos\"]}"
    )

# =========================
# 分散
# =========================
m.execute(
    f"spreadplayers {px} {pz} 8 {R} false "
    f"@e[tag=chestpos]"
)

time.sleep(1)

# =========================
# チェスト設置
# =========================
entities = m.entities("@e[tag=chestpos]")

for e in entities:

    x = math.floor(e["x"])
    y = math.floor(e["y"])
    z = math.floor(e["z"])

    m.execute(
        f"setblock {x} {y} {z} minecraft:chest"
    )

# =========================
# 後始末
# =========================
m.execute("kill @e[tag=chestpos]")

m.echo("✅ ランダムチェスト配置完了")