import minescript as m
import math

# ===== 設定 =====
BLOCK = "minecraft:stone"
DISTANCE = 2

# ===== 向きベクトル計算 =====
def get_facing_vector():
    yaw, pitch = m.player_orientation()
    
    # Yaw を -180～180 に正規化
    yaw = ((yaw + 180) % 360) - 180
    # Pitch を -90～90 に正規化
    pitch = max(min(pitch, 90), -90)

    yaw_rad = math.radians(yaw)
    dx = -math.sin(yaw_rad)
    dz = math.cos(yaw_rad)
    return dx, dz, yaw, pitch

# ===== メイン処理 =====
px, py, pz = map(int, m.player_position())
dx, dz, yaw, pitch = get_facing_vector()

# 前方 DISTANCE ブロック先
tx = px + round(dx * DISTANCE)
ty = py
tz = pz + round(dz * DISTANCE)

# ブロック設置
m.execute(f"/setblock {tx} {ty} {tz} {BLOCK}")

# プレイヤー情報をチャット表示
m.echo(
    f"Pos: {px}, {py}, {pz} | "
    f"Facing: Yaw={yaw:.1f}°, Pitch={pitch:.1f}° | "
    f"Placed {BLOCK} @ {tx}, {ty}, {tz}"
)
