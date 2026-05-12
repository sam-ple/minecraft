import minescript as m
import time

m.execute("gamerule sendCommandFeedback false")

BOSSBAR_ID = "craft_challenge"
player = m.player_name()

# --- チャレンジ設定 ---
CHALLENGES = [
    {"item": "minecraft:compass", "count": 1,
     "materials": [("minecraft:iron_ingot", 4), ("minecraft:redstone", 1)], "time": 20},
    {"item": "minecraft:item_frame", "count": 1,
     "materials": [("minecraft:leather", 1), ("minecraft:stick", 8)], "time": 25},
    {"item": "minecraft:clock", "count": 1,
     "materials": [("minecraft:gold_ingot", 4), ("minecraft:redstone", 1)], "time": 25},
    {"item": "minecraft:fishing_rod", "count": 1,
     "materials": [("minecraft:stick", 3), ("minecraft:string", 2)], "time": 25},
    {"item": "minecraft:anvil", "count": 1,
     "materials": [("minecraft:iron_block", 3), ("minecraft:iron_ingot", 4)], "time": 40},
    {"item": "minecraft:shield", "count": 1,
     "materials": [("minecraft:planks", 6), ("minecraft:iron_ingot", 1)], "time": 25},
    {"item": "minecraft:bookshelf", "count": 1,
     "materials": [("minecraft:book", 3), ("minecraft:planks", 6)], "time": 25},
    {"item": "minecraft:enchanting_table", "count": 1,
     "materials": [("minecraft:book", 1), ("minecraft:diamond", 2), ("minecraft:obsidian", 4)], "time": 40},
]

# --- 前回値のキャッシュ ---
last_bossbar_name = None
last_bossbar_value = None
last_bossbar_max = None

# --- 共通処理 ---
def give_materials(materials):
    m.execute("clear @p")
    time.sleep(0.2)
    for item, count in materials:
        m.execute(f"give @p {item} {count}")

def check_crafted(target, count):
    inv = m.player_inventory()
    total = 0
    for item in inv:
        if getattr(item, "item", "") == target:
            total += item.count
    return total >= count

def format_time(seconds):
    m_ = seconds // 60
    s_ = seconds % 60
    return f"{m_:02}:{s_:02}"

def setup_bossbar():
    m.execute(f"bossbar add {BOSSBAR_ID} {{\"text\":\"Craft Challenge\"}}")
    m.execute(f"bossbar set {BOSSBAR_ID} players @a")

def update_bossbar(text, remaining=None, total=None):
    global last_bossbar_name, last_bossbar_value, last_bossbar_max

    # 時間表示を作成
    if remaining is not None and total is not None:
        time_str = format_time(int(remaining))
        name = f"{text} | ⏳ {time_str}"

        # value 更新
        if int(remaining) != last_bossbar_value:
            m.execute(f"bossbar set {BOSSBAR_ID} value {int(remaining)}")
            last_bossbar_value = int(remaining)

        # max 更新
        if int(total) != last_bossbar_max:
            m.execute(f"bossbar set {BOSSBAR_ID} max {int(total)}")
            last_bossbar_max = int(total)
    else:
        name = text

    # name 更新
    if name != last_bossbar_name:
        m.execute(f"bossbar set {BOSSBAR_ID} name {{\"text\":\"{name}\",\"color\":\"yellow\"}}")
        last_bossbar_name = name

def clear_bossbar():
    m.execute(f"bossbar remove {BOSSBAR_ID}")

# --- カウントダウン表示 ---
def countdown():
    for i in range(3, 0, -1):
        update_bossbar(f"Starting in {i}...")
        time.sleep(1)
    update_bossbar("🚀 Start!")
    time.sleep(1)

# --- メインループ ---
def main():
    setup_bossbar()

    for challenge in CHALLENGES:
        target = challenge["item"]
        count = challenge["count"]
        materials = challenge["materials"]
        time_limit = challenge["time"]

        give_materials(materials)
        countdown()

        start = time.time()

        while True:
            elapsed = time.time() - start
            remaining = max(0, time_limit - elapsed)

            update_bossbar(f"Craft {count} {target}", remaining, time_limit)

            if check_crafted(target, count):
                update_bossbar(f"✅ Success! {target}")
                m.echo(f"🎉 {player} crafted {target}!")
                time.sleep(2)
                break  # 次のチャレンジへ

            if remaining <= 0:
                update_bossbar(f"💀 Game Over! Failed {target}")
                m.echo(f"❌ {player} failed to craft {target}.")
                time.sleep(3)
                clear_bossbar()
                return  # 失敗したら終了

            time.sleep(0.5)

    # 全て成功したら
    update_bossbar("🏆 All Challenges Complete!")
    time.sleep(5)
    clear_bossbar()

if __name__ == "__main__":
    main()
