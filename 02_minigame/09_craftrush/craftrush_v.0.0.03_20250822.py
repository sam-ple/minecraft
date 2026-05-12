import minescript as m
import time

BOSSBAR_ID = "craft_challenge"
player = m.player_name()

# --- チャレンジ設定（リストでまとめる） ---
CHALLENGES = [
    {
        "item": "minecraft:compass",
        "count": 1,
        "materials": [("minecraft:iron_ingot", 4), ("minecraft:redstone", 1)],
        "time": 30
    },
    {
        "item": "minecraft:item_frame",
        "count": 1,
        "materials": [("minecraft:leather", 1), ("minecraft:stick", 8)],
        "time": 30
    },
    {
        "item": "minecraft:clock",
        "count": 1,
        "materials": [("minecraft:gold_ingot", 4), ("minecraft:redstone", 1)],
        "time": 30
    },
    {
        "item": "minecraft:fishing_rod",
        "count": 1,
        "materials": [("minecraft:stick", 3), ("minecraft:string", 2)],
        "time": 30
    },
    {
        "item": "minecraft:anvil",
        "count": 1,
        "materials": [("minecraft:iron_block", 3), ("minecraft:iron_ingot", 4)],
        "time": 45
    },
    {
        "item": "minecraft:shield",
        "count": 1,
        "materials": [("minecraft:planks", 6), ("minecraft:iron_ingot", 1)],
        "time": 30
    },
    {
        "item": "minecraft:bookshelf",
        "count": 1,
        "materials": [("minecraft:book", 3), ("minecraft:planks", 6)],
        "time": 30
    },
    {
        "item": "minecraft:enchanting_table",
        "count": 1,
        "materials": [("minecraft:book", 1), ("minecraft:diamond", 2), ("minecraft:obsidian", 4)],
        "time": 45
    },
]

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

def update_bossbar(name, remaining, total):
    time_str = format_time(int(remaining))
    text = f"{name} | ⏳ {time_str}"
    m.execute(f"bossbar set {BOSSBAR_ID} name {{\"text\":\"{text}\",\"color\":\"yellow\"}}")
    m.execute(f"bossbar set {BOSSBAR_ID} value {int(remaining)}")
    m.execute(f"bossbar set {BOSSBAR_ID} max {int(total)}")

def clear_bossbar():
    m.execute(f"bossbar remove {BOSSBAR_ID}")

def title_subtitle(title, subtitle="", title_color="gold", subtitle_color="aqua"):
    m.execute("title @a clear")
    m.execute(f'title @a title {{"text":"{title}","color":"{title_color}","bold":true}}')
    if subtitle:
        m.execute(f'title @a subtitle {{"text":"{subtitle}","color":"{subtitle_color}","bold":true}}')

# --- メインループ ---
def main():
    setup_bossbar()

    for challenge in CHALLENGES:
        target = challenge["item"]
        count = challenge["count"]
        materials = challenge["materials"]
        time_limit = challenge["time"]

        give_materials(materials)
        title_subtitle("🎮 Craft Challenge!", f"Craft {count} {target} in {time_limit}s")

        start = time.time()

        while True:
            elapsed = time.time() - start
            remaining = max(0, time_limit - elapsed)

            update_bossbar(target, remaining, time_limit)

            if check_crafted(target, count):
                title_subtitle("✅ Success!", f"You crafted {target}!", "green")
                m.echo(f"🎉 {player} crafted {target}!")
                break

            if remaining <= 0:
                title_subtitle("💀 Time's up!", f"Failed {target}", "red")
                m.echo(f"❌ {player} failed to craft {target}.")
                break

            time.sleep(0.5)

        time.sleep(3)  # 次の挑戦まで少し待つ

    clear_bossbar()
    title_subtitle("🏆 All Challenges Done!", "Great work!", "gold")

if __name__ == "__main__":
    main()
