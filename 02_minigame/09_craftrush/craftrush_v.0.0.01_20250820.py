import minescript as m
import time
from queue import Empty
from minescript import EventQueue, EventType

# --- 設定 ---
CRAFT_ITEM = "minecraft:acacia_button"      # クラフト目標アイテム
CRAFT_COUNT = 1                      # 必要個数
REQUIRED_ITEMS = [                   # クラフトに必要な素材
    ("minecraft:acacia_planks", 1),         # 例：木材2個
]
TIME_LIMIT = 30                      # 制限時間（秒）

player = m.player_name()

def give_materials():
    m.execute("clear @p")  # インベントリ初期化
    time.sleep(0.2)
    for item, count in REQUIRED_ITEMS:
        m.execute(f"give @p {item} {count}")

def check_crafted():
    inv = m.player_inventory()
    total = 0
    for item in inv:
        if getattr(item, "item", "") == CRAFT_ITEM:
            total += item.count
    return total >= CRAFT_COUNT

def title_subtitle(title, subtitle="", title_color="gold", subtitle_color="aqua"):
    m.execute("title @a clear")
    m.execute(f'title @a title {{"text":"{title}","color":"{title_color}","bold":true}}')
    if subtitle:
        m.execute(f'title @a subtitle {{"text":"{subtitle}","color":"{subtitle_color}","bold":true}}')

def main():
    give_materials()
    title_subtitle("🎮 Craft Challenge!", f"You have {TIME_LIMIT} seconds to craft {CRAFT_COUNT} {CRAFT_ITEM}s")
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        remaining = max(0, TIME_LIMIT - elapsed)

        # タイマー表示
        m.execute(f'title @a actionbar {{"text":"⏳ Time left: {int(remaining)}s","color":"yellow"}}')

        if check_crafted():
            title_subtitle("✅ Success!", f"You crafted {CRAFT_ITEM}!", "green")
            m.echo(f"🎉 {player} successfully crafted {CRAFT_ITEM}!")
            break

        if remaining <= 0:
            title_subtitle("💀 Time's up!", "Failed to craft in time", "red")
            m.echo(f"❌ {player} failed to craft {CRAFT_ITEM} in time.")
            break

        time.sleep(0.5)

if __name__ == "__main__":
    main()
