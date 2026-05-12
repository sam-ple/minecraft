import minescript as m
import time

PLAYER = m.player_name()
SCORE_OBJ = "adv_points"
FLAG_OBJ = "adv_flag"   # 一時フラグ用
achieved = set()

# スコアボード初期化
existing = m.execute("scoreboard objectives list") or []
if SCORE_OBJ not in "".join(existing):
    m.execute(f"scoreboard objectives add {SCORE_OBJ} dummy AdvPoints")
if FLAG_OBJ not in "".join(existing):
    m.execute(f"scoreboard objectives add {FLAG_OBJ} dummy AdvFlag")

m.execute(f"scoreboard players set {PLAYER} {SCORE_OBJ} 0")
m.execute(f"scoreboard players set {PLAYER} {FLAG_OBJ} 0")

m.echo("🛠 Debug Quest running...")

while True:
    # まだ検知していない場合だけチェック
    if "minecraft:story/mine_diamond" not in achieved:
        # 条件成立時のみフラグ=1
        m.execute(
            f"execute if entity @a[name={PLAYER},advancements={{story/mine_diamond=true}}] "
            f"run scoreboard players set {PLAYER} {FLAG_OBJ} 1"
        )

        # フラグ読み取り
        flag_val = m.execute(f"scoreboard players get {PLAYER} {FLAG_OBJ}")
        if flag_val and "1" in str(flag_val):
            achieved.add("minecraft:story/mine_diamond")
            m.execute(f"scoreboard players add {PLAYER} {SCORE_OBJ} 3")
            m.echo("💎 Diamond unlocked +3pt")

    time.sleep(2.0)
