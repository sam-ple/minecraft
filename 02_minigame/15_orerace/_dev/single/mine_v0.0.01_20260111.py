import minescript as m
import time, sys

ALL_ORES=[
    "coal_ore","deepslate_coal_ore",
    "iron_ore","deepslate_iron_ore",
    "copper_ore","deepslate_copper_ore",
    "gold_ore","deepslate_gold_ore",
    "redstone_ore","deepslate_redstone_ore",
    "lapis_ore","deepslate_lapis_ore",
    "diamond_ore","deepslate_diamond_ore",
    "emerald_ore","deepslate_emerald_ore",
    "nether_quartz_ore"
]

def setup():
    # 既存のスコアボード削除
    try: m.execute("scoreboard objectives remove OreCount")
    except: pass
    for ore in ALL_ORES:
        try: m.execute(f"scoreboard objectives remove mined_{ore}")
        except: pass

    # OreCount スコアボード作成（サイドバー用）
    m.execute('scoreboard objectives add OreCount dummy "Ore Count"')

    # 各鉱石の mined カウント
    for ore in ALL_ORES:
        m.execute(f"scoreboard objectives add mined_{ore} mined:{ore}")

    # サイドバーに表示
    m.execute("scoreboard objectives setdisplay sidebar OreCount")
    m.execute('tellraw @a {"text":"🪨 Ore setup complete","color":"green"}')

def main_loop():
    while True:
        # fake player に各鉱石をコピー
        for ore in ALL_ORES:
            m.execute(f'scoreboard players operation "{ore}" OreCount = @a mined_{ore}')
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "setup":
            setup()
            sys.exit(0)
        if sys.argv[1] == "start":
            main_loop()
            sys.exit(0)
