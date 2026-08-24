import minescript as m
import time

targets = {
    "crocadooo": (100, 100, 100),
    "sampleee": (102, 100, 100),
}

# scoreboard 再作成
m.execute("scoreboard objectives remove XDist")
m.execute('scoreboard objectives add XDist dummy "X Distance"')
m.execute("scoreboard objectives setdisplay sidebar XDist")

UPDATE_INTERVAL = 0.1

while True:
    all_players = m.players(nbt=False)

    for name, fixed_pos in targets.items():
        player_data = [p for p in all_players if p.name == name]
        if not player_data:
            continue

        p = player_data[0]
        px, py, pz = p.position
        fx, fy, fz = fixed_pos

        x_distance = abs(px - fx)

        # ★ 先に登録（これが超重要）
        m.execute(f"scoreboard players add {name} XDist 0")
        m.execute(f"scoreboard players set {name} XDist {int(x_distance)}")

    time.sleep(UPDATE_INTERVAL)
