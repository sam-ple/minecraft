import minescript as m
import time

# ===== 設定 =====
JOB_BLOCK = "minecraft:smithing_table"
DISTANCE = 2          # プレイヤー前方
BOAT_OFFSET = 2       # ボートは横に2ブロック
CHECK_RADIUS = 3      # 存在確認範囲

# ===== 向きベクトル =====
def get_facing_vector():
    yaw = m.player_rotation()[0] % 360
    if 45 <= yaw < 135:
        return (-1, 0)
    elif 135 <= yaw < 225:
        return (0, -1)
    elif 225 <= yaw < 315:
        return (1, 0)
    else:
        return (0, 1)

# ===== プレイヤー前方座標 =====
px, py, pz = map(int, m.player_position())
dx, dz = get_facing_vector()

# 村人座標
vx, vy, vz = px + dx * DISTANCE, py, pz + dz * DISTANCE

# ボート座標（村人横）
bx, bz = vx + dz * BOAT_OFFSET, vz - dx * BOAT_OFFSET

# 職業ブロック座標（村人反対側）
job_x, job_z = vx - dz, vz + dx

# ===== ボート召喚 =====
m.execute(f"/execute unless entity @e[type=minecraft:boat,distance=..{CHECK_RADIUS},x={bx},y={vy},z={bz}] run summon minecraft:boat {bx} {vy} {bz}")

# ===== 求職者村人召喚 =====
m.execute(
    f"/execute unless entity @e[type=minecraft:villager,distance=..{CHECK_RADIUS},x={vx},y={vy},z={vz}] run "
    f"summon minecraft:villager {vx} {vy} {vz} "
    "{{VillagerData:{{profession:none,level:1,type:plains}}}}"
)

time.sleep(0.1)  # 少し待つ

# ===== 村人をボートに乗せる =====
m.execute(
    f"/ride @e[type=minecraft:villager,sort=nearest,limit=1,distance=..{CHECK_RADIUS}] "
    f"mount @e[type=minecraft:boat,sort=nearest,limit=1,distance=..{CHECK_RADIUS}]"
)

# ===== 職業ブロック設置 =====
m.execute(f"/setblock {job_x} {vy} {job_z} {JOB_BLOCK}")

m.echo("👷 村人召喚 → ボート横置き → 職業ブロック設置 完了")
