import minescript as m
import time

# 追跡対象プレイヤーとスタート地点
# タプルは (スタートX, スタートY, スタートZ)
targets = {
    "crocadooo": (100, 100, 100),
    "sampleee": (102, 100, 100),
}

# 安全X範囲の設定（±1ブロックなど）
X_RANGE = 1.5

UPDATE_INTERVAL = 0.1  # チェック間隔（秒）

while True:
    all_players = m.players(nbt=False)

    for name, start_pos in targets.items():
        player_data = [p for p in all_players if p.name == name]
        if not player_data:
            continue
        p = player_data[0]
        px, py, pz = p.position
        sx, sy, sz = start_pos

        # X座標がスタート地点から範囲外ならkillしてTP
        if px < sx - X_RANGE or px > sx + X_RANGE:
            m.execute(f"kill {name}")
            # 少し待ってからスタート地点にTP（kill後リスポーン）
            time.sleep(0.1)
            m.execute(f"tp {name} {sx} {sy} {sz}")
            m.echo(f"{name} went out of X range and has been reset to start!")

    time.sleep(UPDATE_INTERVAL)
