import minescript as m
import time

PLAYER = m.player_name()
SCORE_OBJ = "adv_points"
FLAG_OBJ = "adv_flag"   # 一時フラグ用スコア
achieved = set()

# スコアボードセットアップ
existing = m.execute("scoreboard objectives list") or []
if SCORE_OBJ not in "".join(existing):
    m.execute(f"scoreboard objectives add {SCORE_OBJ} dummy AdvPoints")
if FLAG_OBJ not in "".join(existing):
    m.execute(f"scoreboard objectives add {FLAG_OBJ} dummy AdvFlag")

m.execute(f"scoreboard players set {PLAYER} {SCORE_OBJ} 0")
m.execute(f"scoreboard players set {PLAYER} {FLAG_OBJ} 0")

m.echo("🛠 Debug Quest running...")

while True:
    # まだ未達成ならフラグ更新を試す
    if "minecraft:story/mine_diamond" not in achieved:
        # 条件成立時だけフラグ=1に設定
        m.execute(
            f"execute if entity @a[name={PLAYER},advancements={{story/mine_diamond=true}}] "
            f"run scoreboard players set {PLAYER} {FLAG_OBJ} 1"
        )

        # フラグを読み出し（scoreboard objectives setdisplay なしでも値は保持される）
        flag_val = m.execute(f"scoreboard players get {PLAYER} {FLAG_OBJ}")

        if flag_val and "1" in str(flag_val):  # 値が1なら達成
            achieved.add("minecraft:story/mine_diamond")
            m.execute(f"scoreboard players add {PLAYER} {SCORE_OBJ} 3")
            m.echo("💎 Diamond unlocked +3pt")

            # フラグをリセット
            m.execute(f"scoreboard players set {PLAYER} {FLAG_OBJ} 0")

    time.sleep(2.0)
