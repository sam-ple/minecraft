import minescript as m
import time, sys

# =========================
# 鉱石定義（表示名 : [通常, deepslate]）
# =========================
ORE_GROUPS = {
    "Coal": ["coal_ore", "deepslate_coal_ore"],
    "Iron": ["iron_ore", "deepslate_iron_ore"],
    "Copper": ["copper_ore", "deepslate_copper_ore"],
    "Gold": ["gold_ore", "deepslate_gold_ore"],
    "Redstone": ["redstone_ore", "deepslate_redstone_ore"],
    "Lapis": ["lapis_ore", "deepslate_lapis_ore"],
    "Diamond": ["diamond_ore", "deepslate_diamond_ore"],
    "Emerald": ["emerald_ore", "deepslate_emerald_ore"],
    "Quartz": ["nether_quartz_ore"]
}

# =========================
# セットアップ
# =========================
def setup():
    # 既存削除
    for obj in ["OreCount", "Temp"]:
        try: m.execute(f"scoreboard objectives remove {obj}")
        except: pass

    for ores in ORE_GROUPS.values():
        for ore in ores:
            try: m.execute(f"scoreboard objectives remove mined_{ore}")
            except: pass

    # サイドバー用
    m.execute('scoreboard objectives add OreCount dummy "Ores Mined"')

    # 一時作業用
    m.execute("scoreboard objectives add Temp dummy")

    # mined 統計
    for ores in ORE_GROUPS.values():
        for ore in ores:
            m.execute(f"scoreboard objectives add mined_{ore} mined:{ore}")

    # サイドバー表示
    m.execute("scoreboard objectives setdisplay sidebar OreCount")

    # 初期化（表示行を固定）
    for name in ORE_GROUPS.keys():
        m.execute(f'scoreboard players set "{name}" OreCount 0')

    m.execute('tellraw @a {"text":"🪨 Ore sidebar setup complete","color":"green"}')

# =========================
# メインループ
# =========================
def main_loop():
    while True:
        for display, ores in ORE_GROUPS.items():
            # Temp を 0 に
            m.execute(f'scoreboard players set "{display}" Temp 0')

            # 通常 + deepslate を加算
            for ore in ores:
                m.execute(
                    f'scoreboard players operation "{display}" Temp += @a mined_{ore}'
                )

            # 結果をサイドバーにコピー
            m.execute(
                f'scoreboard players operation "{display}" OreCount = "{display}" Temp'
            )

        time.sleep(1)

# =========================
# エントリーポイント
# =========================
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "setup":
            setup()
            sys.exit(0)
        if sys.argv[1] == "start":
            main_loop()
            sys.exit(0)
