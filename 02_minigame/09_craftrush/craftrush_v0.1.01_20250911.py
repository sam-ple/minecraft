import minescript as m
import time
import random

m.execute("gamerule sendCommandFeedback false")

BOSSBAR_ID = "craft_challenge"
player = m.player_name()

# --- チャレンジ設定（正解のみ定義） ---
CHALLENGES = [
    # --- 武器・ツール ---
    {"item": "minecraft:diamond_sword", "count": 1,
     "materials": [("minecraft:diamond", 2), ("minecraft:stick", 1)], "time": 20},
    {"item": "minecraft:diamond_pickaxe", "count": 1,
     "materials": [("minecraft:diamond", 3), ("minecraft:stick", 2)], "time": 20},
    {"item": "minecraft:diamond_axe", "count": 1,
     "materials": [("minecraft:diamond", 3), ("minecraft:stick", 2)], "time": 20},
    {"item": "minecraft:diamond_shovel", "count": 1,
     "materials": [("minecraft:diamond", 1), ("minecraft:stick", 2)], "time": 15},
    {"item": "minecraft:bow", "count": 1,
     "materials": [("minecraft:stick", 3), ("minecraft:string", 3)], "time": 30},
    {"item": "minecraft:crossbow", "count": 1,
     "materials": [("minecraft:stick", 3), ("minecraft:iron_ingot", 2), ("minecraft:string", 2), ("minecraft:tripwire_hook", 1)], "time": 35},
    {"item": "minecraft:fishing_rod", "count": 1,
     "materials": [("minecraft:stick", 3), ("minecraft:string", 2)], "time": 25},
    
    # --- 防具 ---
    {"item": "minecraft:diamond_helmet", "count": 1,
     "materials": [("minecraft:diamond", 5)], "time": 20},
    {"item": "minecraft:diamond_chestplate", "count": 1,
     "materials": [("minecraft:diamond", 8)], "time": 25},
    {"item": "minecraft:diamond_leggings", "count": 1,
     "materials": [("minecraft:diamond", 7)], "time": 22},
    {"item": "minecraft:diamond_boots", "count": 1,
     "materials": [("minecraft:diamond", 4)], "time": 15},
    {"item": "minecraft:shield", "count": 1,
     "materials": [("minecraft:oak_planks", 6), ("minecraft:iron_ingot", 1)], "time": 25},
    
    # --- 便利ブロック ---
    {"item": "minecraft:enchanting_table", "count": 1,
     "materials": [("minecraft:book", 1), ("minecraft:diamond", 2), ("minecraft:obsidian", 4)], "time": 40},
    {"item": "minecraft:anvil", "count": 1,
     "materials": [("minecraft:iron_block", 3), ("minecraft:iron_ingot", 4)], "time": 40},
    {"item": "minecraft:beacon", "count": 1,
     "materials": [("minecraft:nether_star", 1), ("minecraft:glass", 5), ("minecraft:obsidian", 3)], "time": 50},
    {"item": "minecraft:hopper", "count": 1,
     "materials": [("minecraft:iron_ingot", 5), ("minecraft:chest", 1)], "time": 30},
    {"item": "minecraft:observer", "count": 1,
     "materials": [("minecraft:redstone", 2), ("minecraft:quartz", 1), ("minecraft:stone", 6)], "time": 25},
    {"item": "minecraft:piston", "count": 1,
     "materials": [("minecraft:iron_ingot", 3), ("minecraft:redstone", 1), ("minecraft:oak_planks", 3), ("minecraft:cobblestone", 4)], "time": 30},
    {"item": "minecraft:sticky_piston", "count": 1,
     "materials": [("minecraft:piston", 1), ("minecraft:slime_ball", 1)], "time": 35},
    {"item": "minecraft:redstone_block", "count": 1,
     "materials": [("minecraft:redstone", 9)], "time": 5},
    {"item": "minecraft:redstone_torch", "count": 1,
     "materials": [("minecraft:stick", 1), ("minecraft:redstone", 1)], "time": 3},

    # --- 複雑な装飾・観賞用アイテム ---
    {"item": "minecraft:firework_rocket", "count": 3,
     "materials": [("minecraft:paper", 1), ("minecraft:gunpowder", 1)], "time": 5},
    {"item": "minecraft:firework_star", "count": 1,
     "materials": [("minecraft:gunpowder", 1), ("minecraft:dye", 1)], "time": 5},
    {"item": "minecraft:armor_stand", "count": 1,
     "materials": [("minecraft:stick", 6), ("minecraft:stone_slab", 1)], "time": 15},
    {"item": "minecraft:map", "count": 1,
     "materials": [("minecraft:paper", 8), ("minecraft:compass", 1)], "time": 20},
    {"item": "minecraft:compass", "count": 1,
     "materials": [("minecraft:iron_ingot", 4), ("minecraft:redstone", 1)], "time": 20},
    {"item": "minecraft:clock", "count": 1,
     "materials": [("minecraft:gold_ingot", 4), ("minecraft:redstone", 1)], "time": 25},
    {"item": "minecraft:item_frame", "count": 1,
     "materials": [("minecraft:leather", 1), ("minecraft:stick", 8)], "time": 25},
    {"item": "minecraft:bookshelf", "count": 1,
     "materials": [("minecraft:book", 3), ("minecraft:oak_planks", 6)], "time": 25},

    # --- 食料・面白アイテム ---
    {"item": "minecraft:cake", "count": 1,
     "materials": [("minecraft:milk_bucket", 3), ("minecraft:sugar", 2), ("minecraft:egg", 1), ("minecraft:wheat", 3)], "time": 30},
    {"item": "minecraft:golden_apple", "count": 1,
     "materials": [("minecraft:apple", 1), ("minecraft:gold_ingot", 8)], "time": 25},
    {"item": "minecraft:enchanted_golden_apple", "count": 1,
     "materials": [("minecraft:apple", 1), ("minecraft:gold_block", 8)], "time": 50},

    # --- ネザー関連 ---
    {"item": "minecraft:netherite_ingot", "count": 1,
     "materials": [("minecraft:netherite_scrap", 4), ("minecraft:gold_ingot", 4)], "time": 40},
    {"item": "minecraft:netherite_sword", "count": 1,
     "materials": [("minecraft:diamond_sword", 1), ("minecraft:netherite_ingot", 1)], "time": 35},
    {"item": "minecraft:netherite_pickaxe", "count": 1,
     "materials": [("minecraft:diamond_pickaxe", 1), ("minecraft:netherite_ingot", 1)], "time": 35},
    {"item": "minecraft:lodestone", "count": 1,
     "materials": [("minecraft:netherite_ingot", 8), ("minecraft:chiseled_stone_bricks", 1)], "time": 45},
    {"item": "minecraft:respawn_anchor", "count": 1,
     "materials": [("minecraft:crying_obsidian", 6), ("minecraft:glowstone", 3)], "time": 40},

    # --- エンド関連 ---
    {"item": "minecraft:end_crystal", "count": 1,
     "materials": [("minecraft:glass", 7), ("minecraft:eye_of_ender", 1), ("minecraft:ghast_tear", 1)], "time": 50},
    {"item": "minecraft:elytra", "count": 1,
     "materials": [("minecraft:phantom_membrane", 2)], "time": 50},

    # --- その他ギミック系 ---
    {"item": "minecraft:dropper", "count": 1,
     "materials": [("minecraft:cobblestone", 7), ("minecraft:redstone", 1)], "time": 20},
    {"item": "minecraft:dispenser", "count": 1,
     "materials": [("minecraft:cobblestone", 7), ("minecraft:redstone", 1), ("minecraft:bow", 1)], "time": 25},
    {"item": "minecraft:comparator", "count": 1,
     "materials": [("minecraft:redstone", 3), ("minecraft:nether_quartz", 3), ("minecraft:stone", 3)], "time": 25},
    {"item": "minecraft:repeater", "count": 1,
     "materials": [("minecraft:redstone", 3), ("minecraft:stone", 3), ("minecraft:stone_slab", 2)], "time": 25},
]


# --- ダミー候補（クラフト素材っぽいもの多め） ---
DUMMY_ITEMS = [
    # 🪨 基本資源
    "minecraft:cobblestone",
    "minecraft:stone",
    "minecraft:andesite",
    "minecraft:diorite",
    "minecraft:granite",
    "minecraft:obsidian",
    "minecraft:netherrack",
    "minecraft:end_stone",

    # 🔥 燃料系
    "minecraft:coal",
    "minecraft:charcoal",
    "minecraft:blaze_rod",

    # 📜 軽い素材
    "minecraft:paper",
    "minecraft:string",
    "minecraft:stick",
    "minecraft:bamboo",
    "minecraft:sugar_cane",
    "minecraft:leather",
    "minecraft:rabbit_hide",

    # ⚒ 鉱石系
    "minecraft:flint",
    "minecraft:iron_nugget",
    "minecraft:gold_nugget",
    "minecraft:copper_ingot",
    "minecraft:lapis_lazuli",
    "minecraft:redstone",
    "minecraft:quartz",
    "minecraft:emerald",

    # 🌱 農業系
    "minecraft:wheat",
    "minecraft:potato",
    "minecraft:carrot",
    "minecraft:beetroot",
    "minecraft:pumpkin",
    "minecraft:melon",
    "minecraft:slime_ball",

    # ⚰ モブドロップ
    "minecraft:bone",
    "minecraft:feather",
    "minecraft:gunpowder",
    "minecraft:spider_eye",
    "minecraft:rotten_flesh",
    "minecraft:phantom_membrane",
    "minecraft:ender_pearl",
    "minecraft:ghast_tear",

    # 🟪 ネザー素材
    "minecraft:nether_brick",
    "minecraft:magma_cream",
    "minecraft:glowstone_dust",
    "minecraft:basalt",
    "minecraft:warped_fungus",
    "minecraft:crimson_fungus",

    # 🟨 その他
    "minecraft:glass",
    "minecraft:sand",
    "minecraft:gravel",
    "minecraft:clay_ball",
    "minecraft:sea_pickle",
    "minecraft:prismarine_shard",
    "minecraft:ink_sac",
]


# --- 前回値のキャッシュ ---
last_bossbar_name = None
last_bossbar_value = None
last_bossbar_max = None

# --- 共通処理 ---
def generate_fake_materials(materials):
    """正解素材を含め、合計32種類にして、各アイテム16個ずつに揃える"""
    result = []

    # 正解素材（必ず入れる、数は16固定）
    for item, _ in materials:
        result.append((item, 16))

    # 残りをダミー素材で埋める
    needed = 32 - len(result)
    dummy_choices = random.sample(DUMMY_ITEMS, min(needed, len(DUMMY_ITEMS)))

    for dummy_item in dummy_choices:
        result.append((dummy_item, 16))

    # 万が一足りないときはランダムで補填
    while len(result) < 32:
        dummy_item = random.choice(DUMMY_ITEMS)
        result.append((dummy_item, 16))

    random.shuffle(result)
    return result

def give_materials(materials):
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

    if remaining is not None and total is not None:
        time_str = format_time(int(remaining))
        name = f"{text} | ⏳ {time_str}"

        if int(remaining) != last_bossbar_value:
            m.execute(f"bossbar set {BOSSBAR_ID} value {int(remaining)}")
            last_bossbar_value = int(remaining)

        if int(total) != last_bossbar_max:
            m.execute(f"bossbar set {BOSSBAR_ID} max {int(total)}")
            last_bossbar_max = int(total)
    else:
        name = text

    if name != last_bossbar_name:
        m.execute(f"bossbar set {BOSSBAR_ID} name {{\"text\":\"{name}\",\"color\":\"yellow\"}}")
        last_bossbar_name = name

def clear_bossbar():
    m.execute(f"bossbar remove {BOSSBAR_ID}")

def countdown():
    m.execute("clear @p")  # カウントダウン開始時にアイテムクリア
    for i in range(3, 0, -1):
        update_bossbar(f"Starting in {i}...")
        time.sleep(1)
    update_bossbar("🚀 Start!")

# --- メインループ ---
def main():
    setup_bossbar()

    challenges = CHALLENGES.copy()
    random.shuffle(challenges)  # ここで順番をランダムに

    for challenge in challenges:
        target = challenge["item"]
        count = challenge["count"]
        real_materials = challenge["materials"]
        time_limit = challenge["time"]

        # 偽の材料リストを生成
        fake_materials = generate_fake_materials(real_materials)

        countdown()  # まずカウントダウン
        give_materials(fake_materials)  # Start! と同時に渡す
        start = time.time()

        while True:
            elapsed = time.time() - start
            remaining = max(0, time_limit - elapsed)

            update_bossbar(f"Craft {count} {target}", remaining, time_limit)

            if check_crafted(target, count):
                update_bossbar(f"✅ Success! {target}")
                m.echo(f"🎉 {player} crafted {target}!")
                time.sleep(2)
                break

            if remaining <= 0:
                update_bossbar(f"💀 Game Over! Failed {target}")
                m.echo(f"❌ {player} failed to craft {target}.")
                time.sleep(3)
                clear_bossbar()
                return

            time.sleep(0.5)

    update_bossbar("🏆 All Challenges Complete!")
    time.sleep(5)
    clear_bossbar()

if __name__ == "__main__":
    main()
