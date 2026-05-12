import minescript as m
import time

PLAYER = m.player_name()
SCORE_OBJ = "adv_points"
DEBUG_OBJ = "debug_tmp"
achieved = set()

# スコアボードセットアップ
existing = m.execute("scoreboard objectives list") or []
if SCORE_OBJ not in "".join(existing):
    m.execute(f"scoreboard objectives add {SCORE_OBJ} dummy AdvPoints")
if DEBUG_OBJ not in "".join(existing):
    m.execute(f"scoreboard objectives add {DEBUG_OBJ} dummy DebugTmp")

m.execute(f"scoreboard players set {PLAYER} {SCORE_OBJ} 0")
m.execute(f"scoreboard players set {PLAYER} {DEBUG_OBJ} 0")

m.echo("🛠 Debug Quest running...")

with m.EventQueue() as q:
    q.register_chat_listener()

    while True:
        # まだダイヤ進捗を検知していなければコマンド実行
        if "minecraft:story/mine_diamond" not in achieved:
            m.execute(
                f"execute if entity @a[name={PLAYER},advancements={{story/mine_diamond=true}}] run say __DIAMOND__"
            )

        try:
            event = q.get(timeout=2.0)
            if event.type == m.EventType.CHAT and "__DIAMOND__" in event.message:
                if "minecraft:story/mine_diamond" not in achieved:
                    achieved.add("minecraft:story/mine_diamond")
                    m.execute(f"scoreboard players add {PLAYER} {SCORE_OBJ} 3")
                    m.echo("💎 Diamond unlocked +3pt")
        except:
            pass

        time.sleep(2.0)
