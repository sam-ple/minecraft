import minescript as m
import time
from minescript import EventQueue, EventType

# --- 設定 ---
CRAFT_ITEM = "minecraft:acacia_button"      # クラフト目標アイテム
CRAFT_COUNT = 1                             # 必要個数
REQUIRED_ITEMS = [
    ("minecraft:acacia_planks", 1),
]
TIME_LIMIT = 30                             # 制限時間（秒）

BOSSBAR_ID = "craft_challenge"              # ボスバーID
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

def format_time(seconds: int) -> str:
    """秒を 00:00 形式にフォーマット"""
    m_ = seconds // 60
    s_ = seconds % 60
    return f"{m_:02}:{s_:02}"

def setup_bossbar():
    # ボスバー作成（存在する場合は上書きされる）
    m.execute(f"bossbar add {BOSSBAR_ID} {{\"text\":\"Craft Challenge\"}}")
    m.execute(f"bossbar set {BOSSBAR_ID} players @a")

def update_bossbar(remaining, total):
    # 進捗を計算（0.0〜1.0）
    progress = max(0.0, min(1.0, remaining / total))
    time_str = format_time(int(remaining))
    name = f"Craft {CRAFT_COUNT} {CRAFT_ITEM} | ⏳ {time_str}"
    m.execute(f"bossbar set {BOSSBAR_ID} name {{\"text\":\"{name}\",\"color\":\"yellow\"}}")
    m.execute(f"bossbar set {BOSSBAR_ID} value {int(remaining)}")
    m.execute(f"bossbar set {BOSSBAR_ID} max {int(total)}")
    m.execute(f"bossbar set {BOSSBAR_ID} players @a")
    # progressバーは value/max で表現されるので別指定は不要

def clear_bossbar():
    m.execute(f"bossbar remove {BOSSBAR_ID}")

def title_subtitle(title, subtitle="", title_color="gold", subtitle_color="aqua"):
    m.execute("title @a clear")
    m.execute(f'title @a title {{"text":"{title}","color":"{title_color}","bold":true}}')
    if subtitle:
        m.execute(f'title @a subtitle {{"text":"{subtitle}","color":"{subtitle_color}","bold":true}}')

def main():
    give_materials()
    setup_bossbar()

    title_subtitle("🎮 Craft Challenge!", f"You have {TIME_LIMIT} seconds to craft {CRAFT_COUNT} {CRAFT_ITEM}s")
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        remaining = max(0, TIME_LIMIT - elapsed)

        update_bossbar(remaining, TIME_LIMIT)

        if check_crafted():
            title_subtitle("✅ Success!", f"You crafted {CRAFT_ITEM}!", "green")
            m.echo(f"🎉 {player} successfully crafted {CRAFT_ITEM}!")
            break

        if remaining <= 0:
            title_subtitle("💀 Time's up!", "Failed to craft in time", "red")
            m.echo(f"❌ {player} failed to craft {CRAFT_ITEM} in time.")
            break

        time.sleep(0.5)

    # 終了処理
    clear_bossbar()

if __name__ == "__main__":
    main()
