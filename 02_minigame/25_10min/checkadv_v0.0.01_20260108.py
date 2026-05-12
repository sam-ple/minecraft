import minescript as m
from minescript import EventQueue, EventType

# ==============================
# config
# ==============================
KEY_CODE = 344  # Right Shift
index = 0

m.execute("advancement revoke @a everything")
m.execute("/difficulty easy")
m.execute("/kill @e[type=!player]")
m.execute("/gamerule doMobSpawning false")

# def reset_player():
#     m.execute("/clear @p")
#     m.execute("/effect clear @p")


# ==============================
# ADV test functions
# ==============================

def stone_age():
    m.echo("ADV: Stone Age")
    m.execute("/give @p minecraft:cobblestone")

def upgrade_tools():
    m.echo("ADV: Getting an Upgrade")
    m.execute("/give @p minecraft:stone_pickaxe")

def acquire_hardware():
    m.echo("ADV: Acquire Hardware")
    m.execute("/give @p minecraft:iron_ingot")

def suit_up():
    m.echo("ADV: Suit Up")
    m.execute("/item replace entity @p armor.chest with minecraft:iron_chestplate")

def hot_stuff():
    m.echo("ADV: Hot Stuff")
    m.execute("/give @p minecraft:lava_bucket")

def iron_pick():
    m.echo("ADV: Isn't It Iron Pick")
    m.execute("/give @p minecraft:iron_pickaxe")

def diamonds():
    m.echo("ADV: Diamonds!")
    m.execute("/give @p minecraft:diamond")

def enchanter():
    m.echo("ADV: Enchanter")

def enter_nether():
    m.echo("ADV: Enter the Nether")
    x, y, z = map(int, m.player_position())
    x -= 7
    z += 3

    for dy in range(5):
        for dx in range(4):
            block = "minecraft:obsidian" if dx in (0, 3) or dy in (0, 4) else "minecraft:air"
            m.execute(f"/setblock {x+dx} {y+dy} {z} {block}")

    m.execute(f"/setblock {x+1} {y+1} {z} minecraft:fire")

def monster_hunter():
    m.echo("ADV: Monster Hunter")
    x, y, z = m.player_position()

    # 動かないゾンビ
    m.execute(
        f"/summon minecraft:zombie {x+2} {y} {z} "
        "{NoAI:1b,PersistenceRequired:1b}"
    )

    # プレイヤーにダイヤの斧（オンハンド）
    # m.execute("/give @p minecraft:diamond_axe")
    m.execute("/item replace entity @p weapon.mainhand with minecraft:diamond_axe")

def sweet_dreams():
    m.echo("ADV: Sweet Dreams")
    x, y, z = map(int, m.player_position())

    m.execute("/time set night")

    # m.execute("/give @p minecraft:white_bed")
    # ベッド設置（頭が南向き）
    m.execute(f"/setblock {x+1} {y} {z} minecraft:white_bed[facing=south,part=foot]")
    m.execute(f"/setblock {x+1} {y} {z+1} minecraft:white_bed[facing=south,part=head]")

def trade():
    m.echo("ADV: What a Deal")
    x, y, z = m.player_position()
    m.execute(
        f"/summon minecraft:villager {x+2} {y} {z} "
        "{Invulnerable:1b,Offers:{Recipes:[{buy:{id:emerald,Count:1},sell:{id:apple,Count:1},maxUses:9999}]}}"
    )
    m.execute("/give @p minecraft:emerald 64")

def take_aim():
    m.echo("ADV: Take Aim")
    x, y, z = m.player_position()

    # 動かないスケルトン（攻撃しない）
    m.execute(
        f"/summon minecraft:skeleton {x+6} {y} {z} "
        "{NoAI:1b,PersistenceRequired:1b}"
    )

    # 弓と矢（オンハンド）
    # m.execute("/give @p minecraft:bow")
    m.execute("/give @p minecraft:arrow 64")
    m.execute("/item replace entity @p weapon.mainhand with minecraft:bow")

def ol_betsy():
    m.echo("ADV: Ol' Betsy")
    m.execute("/give @p minecraft:crossbow")

def tame_animal():
    m.echo("ADV: Best Friends Forever")
    x, y, z = m.player_position()
    m.execute(f"/summon minecraft:wolf {x+2} {y} {z} {{NoAI:1b}}")
    m.execute("/give @p minecraft:bone 64")

def not_today_thank_you():
    m.echo("ADV: Not Today, Thank You")
    x, y, z = m.player_position()

    m.execute("/time set night")

    # オフハンドに盾
    m.execute("/item replace entity @p weapon.offhand with minecraft:shield")

    # 動かないが攻撃するスケルトン
    m.execute(
        f"/summon minecraft:skeleton {x+6} {y} {z} "
        "{PersistenceRequired:1b,Attributes:[{Name:generic.movement_speed,Base:0.0}],"
        "HandItems:[{id:bow,Count:1},{}]}"
    )

def plant_seed():
    m.echo("ADV: A Seedy Place")
    m.execute("/item replace entity @p weapon.mainhand with minecraft:diamond_hoe")
    m.execute("/give @p minecraft:wheat_seeds")

def fishy_business():
    m.echo("ADV: Fishy Business")
    m.execute("/give @p minecraft:fishing_rod")

def sniper_prep():
    m.echo("ADV: Sniper Duel (prep)")
    x, y, z = m.player_position()
    m.execute(f"/summon minecraft:skeleton {x+8} {y} {z}")

def ice_bucket_challenge():
    m.echo("ADV: Ice Bucket Challenge")
    m.execute("/give @p minecraft:obsidian")

def cover_me_with_diamonds():
    m.echo("ADV: Cover Me With Diamonds")
    m.execute("/item replace entity @p armor.head with minecraft:diamond_helmet")
    m.execute("/item replace entity @p armor.chest with minecraft:diamond_chestplate")
    m.execute("/item replace entity @p armor.legs with minecraft:diamond_leggings")
    m.execute("/item replace entity @p armor.feet with minecraft:diamond_boots")

def hidden_in_the_depths():
    m.echo("ADV: Hidden in the Depths")
    m.execute("/give @p minecraft:ancient_debris")

def who_is_cutting_onions():
    m.echo("ADV: Who Is Cutting Onions?")
    m.execute("/give @p minecraft:crying_obsidian")

def cover_me_in_debris():
    m.echo("ADV: Cover Me in Debris")
    m.execute("/item replace entity @p armor.head with minecraft:netherite_helmet")
    m.execute("/item replace entity @p armor.chest with minecraft:netherite_chestplate")
    m.execute("/item replace entity @p armor.legs with minecraft:netherite_leggings")
    m.execute("/item replace entity @p armor.feet with minecraft:netherite_boots")

def spooky_scary_skeleton():
    m.echo("ADV: Spooky Scary Skeleton")
    m.execute("/give @p minecraft:wither_skeleton_skull")

def into_fire():
    m.echo("ADV: Into Fire")
    m.execute("/give @p minecraft:blaze_rod")

def the_next_generation():
    m.echo("ADV: The Next Generation")
    m.execute("/give @p minecraft:dragon_egg")

def you_need_a_mint():
    m.echo("ADV: You Need a Mint")
    m.execute("/give @p minecraft:dragon_breath")

def sky_is_the_limit_equip():
    m.echo("ADV: Sky's the Limit")
    m.execute("/item replace entity @p armor.chest with minecraft:elytra")

# ==============================
# ADV execution order
# ==============================
ADV_TESTS = [
    stone_age,
    upgrade_tools,
    acquire_hardware,
    suit_up,
    hot_stuff,
    iron_pick,
    diamonds,
    # enchanter,
    # enter_nether,
    monster_hunter,
    sweet_dreams,
    # trade,
    # take_aim,
    # ol_betsy,
    tame_animal,
    # not_today_thank_you,
    plant_seed,
    # fishy_business,
    # sniper_prep,
    ice_bucket_challenge,
    cover_me_with_diamonds,
    hidden_in_the_depths,
    who_is_cutting_onions,
    cover_me_in_debris,
    spooky_scary_skeleton,
    into_fire,
    the_next_generation,
    you_need_a_mint,
    sky_is_the_limit_equip,
]

# ==============================
# key loop
# ==============================
with EventQueue() as eq:
    eq.register_key_listener()
    m.echo("🧪 ADV TEST MODE")
    m.echo("➡ Right Shift = next advancement setup")

    while True:
        event = eq.get()
        if event.type == EventType.KEY and event.action == 0 and event.key == KEY_CODE:
            m.echo("-----------------------")
            # m.echo(f"▶ {ADV_TESTS[index].__name__}")
            m.echo(f"▶ [{index+1}/{len(ADV_TESTS)}] {ADV_TESTS[index].__name__}")
            ADV_TESTS[index]()
            index = (index + 1) % len(ADV_TESTS)
