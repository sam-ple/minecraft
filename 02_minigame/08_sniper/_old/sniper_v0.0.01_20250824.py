import minescript as m
from minescript import EventQueue, EventType
import time, math

PLAYER = m.player_name()

# --- 調整用パラメータ ---
RANGE = 120          # 射程（ブロック）
DAMAGE = 20          # 基本ダメージ
COOLDOWN = 0.5       # 連射間隔（秒）
HITBOX = 0.7         # 命中判定の半径（ブロック）

m.execute("gamerule sendCommandFeedback false")

def spyglass_in_mainhand():
    hands = m.player_hand_items()
    if not hands or not hands.main_hand:
        return False

    # dict or str 両対応
    if isinstance(hands.main_hand, dict):
        item = hands.main_hand.get("item", None)
    else:
        item = str(hands.main_hand)

    return item == "minecraft:spyglass"

def dir_from_yaw_pitch(yaw, pitch):
    # Minecraftの向き → 単位ベクトル
    ry = math.radians(-yaw - 180)
    rp = math.radians(-pitch)
    x = math.sin(ry) * math.cos(rp)
    y = math.sin(rp)
    z = math.cos(ry) * math.cos(rp)
    return (x, y, z)

def eye_pos():
    x, y, z = m.player_position()   # ← 引数なしで呼ぶ
    yaw, pitch = m.player_orientation()

    # プレイヤーの目の高さは 1.62 ブロック分上
    y += 1.62

    return x, y, z, yaw, pitch

def tracer_to(tx, ty, tz):
    # プレイヤーの目→目標まで簡易トレーサー（end_rod）
    ex, ey, ez = eye_pos()
    dist = max(1.0, math.dist((ex, ey, ez), (tx, ty, tz)))
    steps = min(80, int(dist * 2))  # 1ブロックあたり2粒、上限少し抑える
    for i in range(1, steps + 1):
        d = dist * (i / steps)
        m.execute(
            f"execute as {PLAYER} at @s anchored eyes facing {tx} {ty} {tz} "
            f"positioned ^ ^ ^{d} run particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1 force"
        )

def fire():
    ex, ey, ez, yaw, pitch = eye_pos()

    # レイキャスト処理ここに書く（最大距離20とか）
    target = m.player_get_targeted_entity(20)
    if target:
        tx, ty, tz = target.position
        m.execute(f"particle minecraft:crit {tx} {ty+1} {tz} 0 0 0 0 1 force")
        m.execute(f"damage {target.uuid} 20 minecraft:generic")
        m.echo(f"💥 Hit {target.type} for 20 damage!")
    else:
        m.execute(f"particle minecraft:smoke {ex} {ey} {ez} 0 0 0 0 5 force")
        m.echo("💨 Missed...")

def main():
    m.echo("🎯 スナイパー（Spyglass）：右クリックで発射 / ヒットスキャン方式")
    with EventQueue() as eq:
        eq.register_mouse_listener()
        last_shot = 0.0
        while True:
            e = eq.get()
            # 右クリック押下（button:1, action:1）で発射
            if e.type == EventType.MOUSE and e.button == 1 and e.action == 1:
                if not spyglass_in_mainhand():
                    continue
                now = time.time()
                if now - last_shot < COOLDOWN:
                    continue
                last_shot = now
                fire()

main()
