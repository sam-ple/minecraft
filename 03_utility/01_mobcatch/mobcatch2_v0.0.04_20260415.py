import minescript as m
import time

TICK_DELAY = 0.5
ITEM = "minecraft:carrot_on_a_stick"
DIST = 1.5   # ← スケルトン対策（少し手前）
TP_Y = -64

# ==============================
# 全モブ対応MAP
# ==============================
SPAWN_EGG_MAP = {
    "minecraft:allay":"minecraft:allay_spawn_egg",
    "minecraft:armadillo":"minecraft:armadillo_spawn_egg",
    "minecraft:axolotl":"minecraft:axolotl_spawn_egg",
    "minecraft:bat":"minecraft:bat_spawn_egg",
    "minecraft:bee":"minecraft:bee_spawn_egg",
    "minecraft:blaze":"minecraft:blaze_spawn_egg",
    "minecraft:bogged":"minecraft:bogged_spawn_egg",
    "minecraft:breeze":"minecraft:breeze_spawn_egg",
    "minecraft:camel":"minecraft:camel_spawn_egg",
    "minecraft:cat":"minecraft:cat_spawn_egg",
    "minecraft:cave_spider":"minecraft:cave_spider_spawn_egg",
    "minecraft:chicken":"minecraft:chicken_spawn_egg",
    "minecraft:cod":"minecraft:cod_spawn_egg",
    "minecraft:cow":"minecraft:cow_spawn_egg",
    "minecraft:creaking":"minecraft:creaking_spawn_egg",
    "minecraft:creeper":"minecraft:creeper_spawn_egg",
    "minecraft:dolphin":"minecraft:dolphin_spawn_egg",
    "minecraft:donkey":"minecraft:donkey_spawn_egg",
    "minecraft:drowned":"minecraft:drowned_spawn_egg",
    "minecraft:elder_guardian":"minecraft:elder_guardian_spawn_egg",
    "minecraft:ender_dragon":"minecraft:ender_dragon_spawn_egg",
    "minecraft:enderman":"minecraft:enderman_spawn_egg",
    "minecraft:endermite":"minecraft:endermite_spawn_egg",
    "minecraft:evoker":"minecraft:evoker_spawn_egg",
    "minecraft:fox":"minecraft:fox_spawn_egg",
    "minecraft:frog":"minecraft:frog_spawn_egg",
    "minecraft:ghast":"minecraft:ghast_spawn_egg",
    "minecraft:glow_squid":"minecraft:glow_squid_spawn_egg",
    "minecraft:goat":"minecraft:goat_spawn_egg",
    "minecraft:guardian":"minecraft:guardian_spawn_egg",
    "minecraft:hoglin":"minecraft:hoglin_spawn_egg",
    "minecraft:horse":"minecraft:horse_spawn_egg",
    "minecraft:husk":"minecraft:husk_spawn_egg",
    "minecraft:iron_golem":"minecraft:iron_golem_spawn_egg",
    "minecraft:llama":"minecraft:llama_spawn_egg",
    "minecraft:magma_cube":"minecraft:magma_cube_spawn_egg",
    "minecraft:mooshroom":"minecraft:mooshroom_spawn_egg",
    "minecraft:mule":"minecraft:mule_spawn_egg",
    "minecraft:ocelot":"minecraft:ocelot_spawn_egg",
    "minecraft:panda":"minecraft:panda_spawn_egg",
    "minecraft:parrot":"minecraft:parrot_spawn_egg",
    "minecraft:phantom":"minecraft:phantom_spawn_egg",
    "minecraft:pig":"minecraft:pig_spawn_egg",
    "minecraft:piglin":"minecraft:piglin_spawn_egg",
    "minecraft:piglin_brute":"minecraft:piglin_brute_spawn_egg",
    "minecraft:pillager":"minecraft:pillager_spawn_egg",
    "minecraft:polar_bear":"minecraft:polar_bear_spawn_egg",
    "minecraft:pufferfish":"minecraft:pufferfish_spawn_egg",
    "minecraft:rabbit":"minecraft:rabbit_spawn_egg",
    "minecraft:ravager":"minecraft:ravager_spawn_egg",
    "minecraft:salmon":"minecraft:salmon_spawn_egg",
    "minecraft:sheep":"minecraft:sheep_spawn_egg",
    "minecraft:shulker":"minecraft:shulker_spawn_egg",
    "minecraft:silverfish":"minecraft:silverfish_spawn_egg",
    "minecraft:skeleton":"minecraft:skeleton_spawn_egg",
    "minecraft:skeleton_horse":"minecraft:skeleton_horse_spawn_egg",
    "minecraft:slime":"minecraft:slime_spawn_egg",
    "minecraft:sniffer":"minecraft:sniffer_spawn_egg",
    "minecraft:snow_golem":"minecraft:snow_golem_spawn_egg",
    "minecraft:spider":"minecraft:spider_spawn_egg",
    "minecraft:squid":"minecraft:squid_spawn_egg",
    "minecraft:stray":"minecraft:stray_spawn_egg",
    "minecraft:strider":"minecraft:strider_spawn_egg",
    "minecraft:tadpole":"minecraft:tadpole_spawn_egg",
    "minecraft:trader_llama":"minecraft:trader_llama_spawn_egg",
    "minecraft:tropical_fish":"minecraft:tropical_fish_spawn_egg",
    "minecraft:turtle":"minecraft:turtle_spawn_egg",
    "minecraft:vex":"minecraft:vex_spawn_egg",
    "minecraft:vindicator":"minecraft:vindicator_spawn_egg",
    "minecraft:villager":"minecraft:villager_spawn_egg",
    "minecraft:wandering_trader":"minecraft:wandering_trader_spawn_egg",
    "minecraft:warden":"minecraft:warden_spawn_egg",
    "minecraft:witch":"minecraft:witch_spawn_egg",
    "minecraft:wither":"minecraft:wither_spawn_egg",
    "minecraft:wither_skeleton":"minecraft:wither_skeleton_spawn_egg",
    "minecraft:wolf":"minecraft:wolf_spawn_egg",
    "minecraft:zoglin":"minecraft:zoglin_spawn_egg",
    "minecraft:zombie":"minecraft:zombie_spawn_egg",
    "minecraft:zombie_horse":"minecraft:zombie_horse_spawn_egg",
    "minecraft:zombified_piglin":"minecraft:zombified_piglin_spawn_egg",
    "minecraft:zombie_villager":"minecraft:zombie_villager_spawn_egg",
}

# ==============================
# Scoreboard
# ==============================
m.execute("scoreboard objectives add used minecraft.used:carrot_on_a_stick")
m.execute("scoreboard objectives add used_prev dummy")

while True:

    players = m.players()

    # ==========================
    # ① 視線検知（精度UP）
    # ==========================
    for p in players:
        name = p.name
        tag = f"target_{name}"

        # タグリセット
        m.execute(f"tag @e[tag={tag}] remove {tag}")

        # 視線検知（距離＆位置調整）
        m.execute(
            f'execute as @a[name={name}] '
            f'if entity @s[nbt={{SelectedItem:{{id:"{ITEM}"}}}}] '
            f'at @s anchored eyes positioned ^ ^ ^{DIST} '
            f'run tag @e[type=!player,type=!armor_stand,limit=1,sort=nearest,distance=..2] add {tag}'
        )

        # 光る
        m.execute(f"effect give @e[tag={tag}] glowing 1 1 true")

        # # デバッグ表示（名前）
        # m.execute(
        #     f'data merge entity @e[tag={tag},limit=1] '
        #     f'{{CustomName:\'{"TARGET"}\',CustomNameVisible:1b}}'
        # )

        # デバッグパーティクル
        m.execute(
            f'execute at @e[tag={tag}] run particle minecraft:happy_villager ~ ~1 ~ 0.2 0.2 0.2 0 3'
        )

    # ==========================
    # ② クリック検知
    # ==========================
    m.execute('execute as @a if score @s used > @s used_prev run tag @s add just_clicked')

    # ==========================
    # ③ 捕獲処理
    # ==========================
    for p in players:
        name = p.name
        tag = f"target_{name}"

        # --- 卵付与 ---
        for mob, egg in SPAWN_EGG_MAP.items():
            m.execute(
                f'execute as @a[name={name},tag=just_clicked] '
                f'if entity @e[tag={tag},type={mob}] '
                f'run give @s {egg} 1'
            )

        # --- 捕獲演出 ---
        m.execute(
            f'execute as @a[name={name},tag=just_clicked] '
            f'if entity @e[tag={tag}] '
            f'at @e[tag={tag},limit=1] run particle minecraft:portal ~ ~1 ~ 0.5 0.5 0.5 0.2 50'
        )

        m.execute(
            f'execute as @a[name={name},tag=just_clicked] '
            f'if entity @e[tag={tag}] '
            f'run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1'
        )

        # --- ドロップ完全無効化 ---
        m.execute(
            f'execute as @a[name={name},tag=just_clicked] '
            f'if entity @e[tag={tag}] '
            f'run data merge entity @e[tag={tag},limit=1] '
            f'{{DeathLootTable:"minecraft:empty",HandItems:[],ArmorItems:[]}}'
        )

        # --- 見えない位置へ ---
        m.execute(
            f'execute as @a[name={name},tag=just_clicked] '
            f'if entity @e[tag={tag}] '
            f'run tp @e[tag={tag},limit=1] ~ {TP_Y} ~'
        )

        # --- 安全kill ---
        m.execute(
            f'execute as @a[name={name},tag=just_clicked] '
            f'if entity @e[tag={tag}] '
            f'run kill @e[tag={tag},limit=1]'
        )

    # ==========================
    # ④ 後処理
    # ==========================
    m.execute("tag @a[tag=just_clicked] remove just_clicked")
    m.execute("execute as @a run scoreboard players operation @s used_prev = @s used")

    time.sleep(TICK_DELAY)
