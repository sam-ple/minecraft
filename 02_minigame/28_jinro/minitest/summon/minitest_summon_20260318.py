import minescript as m
import math

# =========================
# プレイヤー情報
# =========================
player = m.player()
px, py, pz = player.position

px = math.floor(px)
pz = math.floor(pz)

# =========================
# 設定
# =========================
WORLD_BORDER_RADIUS = 50
NUM_SKELETONS = 10

# ワールドボーダー
m.execute(f"worldborder center {px} {pz}")
m.execute(f"worldborder set {WORLD_BORDER_RADIUS * 2}")

# =========================
# ① 上空に召喚
# =========================
for _ in range(NUM_SKELETONS):
    # m.execute(
    #     f"summon minecraft:skeleton {px} {py+5} {pz} "
    #     "{NoAI:0b,Invulnerable:1b}"
    # )
    m.execute(f"summon minecraft:skeleton {px} {py+5} {pz} "
              "{NoAI:1b,PersistenceRequired:1b,Health:2f}")


# =========================
# ② 分散
# =========================
m.execute(
    f"spreadplayers {px} {pz} 10 {WORLD_BORDER_RADIUS} false "
    f"@e[type=minecraft:skeleton,sort=nearest,limit={NUM_SKELETONS}]"
)

# =========================
# ③ 固定
# =========================
m.execute(
    "execute as @e[type=minecraft:skeleton] run data merge entity @s {NoAI:1b}"
)

m.echo(f"✅ スケルトン {NUM_SKELETONS}体を安全に分散配置しました")
