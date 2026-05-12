import minescript as m
import sys, time

# ==============================
# entry
# ==============================
if len(sys.argv) < 2:
    m.echo("Usage: /ms run check <iron|adv|nether|inv>")
    sys.exit(0)

MODE = sys.argv[1]

# ==============================
# iron : フル鉄装備チェック用
# ※ わざと gold chestplate を混ぜて失敗させる
# ==============================
def test_iron():
    m.echo("⛓ Giving armor (INTENTIONAL FAIL INCLUDED)")

    m.execute("/clear @p")
    m.execute("/give @p minecraft:iron_helmet")
    m.execute("/give @p minecraft:iron_chestplate")
    m.execute("/give @p minecraft:diamond_chestplate")  # ❌ 意図的
    m.execute("/give @p minecraft:iron_leggings")
    m.execute("/give @p minecraft:iron_boots")

    m.echo("⚠ diamond chestplate included intentionally")

# ==============================
# adv : 達成しやすい進捗を順に踏ませる
# ==============================
ADV_ACTIONS = [
    ("Stone Age", lambda: m.execute("/give @p minecraft:cobblestone")),
    ("Upgrade Tools", lambda: m.execute("/give @p minecraft:stone_pickaxe")),
    ("Hot Stuff", lambda: m.execute("/give @p minecraft:lava_bucket")),
    ("Diamonds!", lambda: m.execute("/give @p minecraft:diamond")),
    ("Into Fire", lambda: m.execute("/give @p minecraft:blaze_rod")),
]

def test_adv():
    m.echo("📘 Resetting advancements")
    m.execute("advancement revoke @a everything")
    m.execute("clear @p")

    m.echo("📘 Triggering advancement actions every 2s")

    for name, action in ADV_ACTIONS:
        m.echo(f"▶ trying: {name}")
        action()
        time.sleep(2)

    m.echo("✅ ADV test sequence finished")

# ==============================
# nether : プレイヤー前にネザーゲート生成
# ==============================
def test_nether():
    m.echo("🔥 Creating Nether Portal (blocks will be replaced)")

    x, y, z = m.player_position()

    # 向きを南に固定
    m.execute(f"/tp @p {int(x)} {int(y)} {int(z)} 0 0")

    # プレイヤー前方
    x, y, z = int(x - 7), int(y), int(z + 3)

    # フレーム（高さ5 × 幅4）
    for dy in range(5):
        for dx in range(4):
            bx = x + dx
            by = y + dy
            bz = z

            if dx == 0 or dx == 3 or dy == 0 or dy == 4:
                m.execute(f"/setblock {bx} {by} {bz} minecraft:obsidian")
            else:
                m.execute(f"/setblock {bx} {by} {bz} minecraft:air")

    # 着火
    m.execute(f"/setblock {x + 1} {y + 1} {z} minecraft:fire")

    m.echo("🔥 Nether portal created")

# ==============================
# inv : インベントリを埋める
# ※ わざと重複アイテムを含める
# ==============================
INV_ITEMS = [
    "stone","dirt","cobblestone","oak_log","oak_planks","stick",
    "coal","iron_ingot","gold_ingot","diamond","emerald","lapis_lazuli",
    "redstone","quartz","flint","feather","string","leather",
    "bone","rotten_flesh","gunpowder","paper","book","apple",
    "bread","carrot","potato","baked_potato","torch","bucket",
    "water_bucket","lava_bucket","shears","bow","arrow","arrow"  # ❌ 重複
]

def test_inv():
    m.echo("🎒 Filling inventory (INTENTIONAL DUPLICATE INCLUDED)")
    m.execute("/clear @p")

    for item in INV_ITEMS:
        m.execute(f"/give @p minecraft:{item} 1")
        time.sleep(0.05)

    m.echo("⚠ duplicate item included intentionally")

# ==============================
# dispatch
# ==============================
if MODE == "iron":
    test_iron()
elif MODE == "adv":
    test_adv()
elif MODE == "nether":
    test_nether()
elif MODE == "inv":
    test_inv()
else:
    m.echo(f"Invalid mode: {MODE}")
