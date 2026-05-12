import minescript as m
import random

# プレイヤー位置取得
px, py, pz = m.player_position()

RADIUS_XZ = 5
RADIUS_Y = 3

positions = []
for dx in range(-RADIUS_XZ, RADIUS_XZ + 1):
    for dy in range(-RADIUS_Y, RADIUS_Y + 1):
        for dz in range(-RADIUS_XZ, RADIUS_XZ + 1):
            x = int(px) + dx
            y = int(py) + dy
            z = int(pz) + dz
            positions.append([x, y - 1, z])  # 地面
            positions.append([x, y, z])      # 設置位置
            positions.append([x, y + 1, z])  # 頭上

# 周囲のチャンクを読み込む
m.await_loaded_region(int(px - RADIUS_XZ), int(pz - RADIUS_XZ), int(px + RADIUS_XZ), int(pz + RADIUS_XZ))
block_types = m.getblocklist(positions)

chest_candidates = []
for i in range(0, len(positions), 3):
    below = block_types[i]
    current = block_types[i + 1]
    above = block_types[i + 2]
    if below != "minecraft:air" and current == "minecraft:air" and above == "minecraft:air":
        chest_candidates.append(positions[i + 1])  # 中央座標に設置

# 最大10個までランダムに設置
MAX_CHESTS = 10
random.shuffle(chest_candidates)
count = 0
for pos in chest_candidates:
    if count >= MAX_CHESTS:
        break
    x, y, z = map(int, pos)
    m.execute(f"setblock {x} {y} {z} chest")
    count += 1

m.echo(f"📦 Placed {count} chest(s) nearby.")


import minescript as m
import random

# プレイヤー位置取得
px, py, pz = m.player_position()

RADIUS_XZ = 5
RADIUS_Y = 3

positions = []
for dx in range(-RADIUS_XZ, RADIUS_XZ + 1):
    for dy in range(-RADIUS_Y, RADIUS_Y + 1):
        for dz in range(-RADIUS_XZ, RADIUS_XZ + 1):
            x = int(px) + dx
            y = int(py) + dy
            z = int(pz) + dz
            positions.append([x, y - 1, z])  # 地面
            positions.append([x, y, z])      # モブ設置位置
            positions.append([x, y + 1, z])  # 頭上

m.await_loaded_region(int(px - RADIUS_XZ), int(pz - RADIUS_XZ), int(px + RADIUS_XZ), int(pz + RADIUS_XZ))
block_types = m.getblocklist(positions)

spawn_candidates = []
for i in range(0, len(positions), 3):
    below = block_types[i]
    current = block_types[i + 1]
    above = block_types[i + 2]
    if below != "minecraft:air" and current == "minecraft:air" and above == "minecraft:air":
        spawn_candidates.append(positions[i + 1])

# 最大 10体までランダムに召喚
MAX_SPAWN = 10
random.shuffle(spawn_candidates)
count = 0
for pos in spawn_candidates:
    if count >= MAX_SPAWN:
        break
    x, y, z = pos
    m.execute(f"summon skeleton {x} {y} {z} {{PersistenceRequired:1b}}")
    count += 1

m.echo(f"✅ スケルトン {count} 体召喚しました。")


#------------
# v0.0.1
#------------

# import minescript as m
# import random

# # プレイヤー位置取得（中心）
# px, py, pz = m.player_position()

# # スキャン範囲
# RADIUS_XZ = 5
# RADIUS_Y = 3

# positions = []
# for dx in range(-RADIUS_XZ, RADIUS_XZ + 1):
#     for dy in range(-RADIUS_Y, RADIUS_Y + 1):
#         for dz in range(-RADIUS_XZ, RADIUS_XZ + 1):
#             x = int(px) + dx
#             y = int(py) + dy
#             z = int(pz) + dz
#             positions.append([x, y - 1, z])  # 地面
#             positions.append([x, y, z])      # モブ設置位置
#             positions.append([x, y + 1, z])  # 頭上

# # チャンクの読み込みを待機（高速化）
# m.await_loaded_region(int(px - RADIUS_XZ), int(pz - RADIUS_XZ), int(px + RADIUS_XZ), int(pz + RADIUS_XZ))

# # ブロック情報取得
# block_types = m.getblocklist(positions)

# # 有効なスポーン候補を探す
# spawn_candidates = []
# for i in range(0, len(positions), 3):
#     below = block_types[i]
#     current = block_types[i + 1]
#     above = block_types[i + 2]
#     if below != "minecraft:air" and current == "minecraft:air" and above == "minecraft:air":
#         spawn_candidates.append(positions[i + 1])

# # ランダムに召喚
# if spawn_candidates:
#     x, y, z = random.choice(spawn_candidates)
#     m.execute(f"summon skeleton {x} {y} {z} {{PersistenceRequired:1b}}")
#     m.echo(f"スケルトン召喚: {x} {y} {z}")
# else:
#     m.echo("召喚できる空きスペースが見つかりませんでした。")
