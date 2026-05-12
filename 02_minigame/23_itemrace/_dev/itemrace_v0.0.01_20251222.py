import minescript as m
import time

# ==================================================
# 設定
# ==================================================
TICK_DELAY = 2  # ループ間隔（秒）

TEST_MODE = True
TEST_PLAYERS = ["crocadooo", "saaample"]

TARGET_ITEMS = [
    "minecraft:diamond",
    "minecraft:gold_ingot",
]

# ==================================================
# ヘルパー
# ==================================================
def fmt(item: str) -> str:
    return item.replace("minecraft:", "").replace(":", "_")

def cmd(c: str):
    m.execute(c)

def targets():
    return TEST_PLAYERS if TEST_MODE else ["@a"]

# ==================================================
# scoreboard 初期化
# ==================================================

# スニーク判定用
cmd('scoreboard objectives add sneak_time minecraft.custom:minecraft.sneak_time')
cmd("scoreboard objectives add sneak_prev dummy")
cmd("scoreboard objectives add is_sneaking dummy")
cmd("scoreboard objectives add sneak_edge dummy")  # 0=非スニーク, 1=スニーク開始

# ポイント
cmd("scoreboard objectives add points dummy")
cmd("scoreboard objectives setdisplay sidebar points")

# アイテム用
for item in TARGET_ITEMS:
    name = fmt(item)
    cmd(f"scoreboard objectives add has_{name} dummy")
    cmd(f"scoreboard objectives add collected_{name} dummy")

# 初期化
for t in targets():
    cmd(f"scoreboard players reset {t} sneak_prev")
    cmd(f"scoreboard players reset {t} is_sneaking")
    cmd(f"scoreboard players reset {t} sneak_edge")
    cmd(f"scoreboard players reset {t} points")

    for item in TARGET_ITEMS:
        name = fmt(item)
        cmd(f"scoreboard players reset {t} has_{name}")
        cmd(f"scoreboard players reset {t} collected_{name}")

# ==================================================
# メインループ
# ==================================================
m.echo("🕹️ ItemRace started (safe mode, tellraw disabled)")

while True:

    # ------------------------------
    # スニーク判定
    # ------------------------------
    # sneak_time が前回より大きければスニーク中
    cmd('execute as @a if score @s sneak_time > @s sneak_prev run scoreboard players set @s is_sneaking 1')
    cmd('execute as @a unless score @s sneak_time > @s sneak_prev run scoreboard players set @s is_sneaking 0')

    # sneak_edge = 0→1 の検出
    cmd('execute as @a if score @s is_sneaking matches 1 if score @s sneak_edge matches 0 run scoreboard players set @s sneak_edge 1')
    cmd('execute as @a unless score @s is_sneaking matches 1 run scoreboard players set @s sneak_edge 0')

    # ------------------------------
    # アイテム判定 & 加点
    # ------------------------------
    for t in targets():
        for item in TARGET_ITEMS:
            name = fmt(item)

            # 今持っているか
            cmd(f'execute as {t} if entity @s[nbt={{SelectedItem:{{id:"{item}"}}}}] run scoreboard players set @s has_{name} 1')
            cmd(f'execute as {t} unless entity @s[nbt={{SelectedItem:{{id:"{item}"}}}}] run scoreboard players set @s has_{name} 0')

            # sneak_edge = 1 のとき初取得のみ加点
            cmd(f'execute as {t} if score @s sneak_edge matches 1 if score @s has_{name} matches 1 unless score @s collected_{name} matches 1 run scoreboard players add @s points 1')
            cmd(f'execute as {t} if score @s sneak_edge matches 1 if score @s has_{name} matches 1 unless score @s collected_{name} matches 1 run scoreboard players set @s collected_{name} 1')

    # ------------------------------
    # sneak_prev 更新
    # ------------------------------
    cmd('execute as @a run scoreboard players operation @s sneak_prev = @s sneak_time')

    time.sleep(TICK_DELAY)
