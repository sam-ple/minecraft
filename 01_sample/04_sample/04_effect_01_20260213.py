import minescript as m
import time

# =========================
# 1. 複数エフェクト付与
# =========================

effects = [
    "minecraft:speed 30 1 true",        # Speed II 30秒
    "minecraft:jump_boost 30 2 true",   # Jump Boost III
    "minecraft:slow_falling 30 0 true"  # 落下速度低下
]

for eff in effects:
    m.execute(f"/effect give @p {eff}")
    time.sleep(0.05)

m.echo("Effects granted")

time.sleep(0.2)  # 反映待ち

# =========================
# 2. プレイヤーNBT取得
# =========================

p = m.player(nbt=True)

if not p or not p.nbt:
    print("NBT not available")
    exit()

nbt = p.nbt

# =========================
# 3. 全NBT出力
# =========================

print("========== RAW PLAYER NBT ==========")
print(nbt)
print("====================================")

m.echo("📦 NBT dump complete")
